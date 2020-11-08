import asyncio
import discord


class CannotPaginate(Exception):
    pass


class Pages:
    def __init__(self, ctx, *, entries, per_page=12, show_entry_count=True, numsbool=True, embedcolor="blurple", thumbnail=None):
        self.bot = ctx.bot
        self.entries = entries
        self.message = ctx.message
        self.channel = ctx.channel
        self.author = ctx.author
        self.per_page = per_page
        self.numsbool = numsbool
        pages, left_over = divmod(len(self.entries), self.per_page)
        if left_over:
            pages += 1
        self.maximum_pages = pages
        if embedcolor == "blurple":
            colour = discord.Colour.blurple()
        elif embedcolor == "orange":
            colour = discord.Colour.orange()
        self.embed = discord.Embed(colour=colour)
        self.paginating = len(entries) > per_page
        self.show_entry_count = show_entry_count
        if thumbnail is not None:
            self.embed.set_thumbnail(url=thumbnail)
        self.reaction_emojis = [
            ("\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}",
             self.first_page),
            ("\N{BLACK LEFT-POINTING TRIANGLE}", self.previous_page),
            ("\N{BLACK RIGHT-POINTING TRIANGLE}", self.next_page),
            ("\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}",
             self.last_page),
            ("\N{INPUT SYMBOL FOR NUMBERS}", self.numbered_page),
            ("\N{BLACK SQUARE FOR STOP}", self.stop_pages),
            ("\N{INFORMATION SOURCE}", self.show_help),
        ]

        if ctx.guild is not None:
            self.permissions = self.channel.permissions_for(ctx.guild.me)
        else:
            self.permissions = self.channel.permissions_for(ctx.bot.user)
  
    def get_page(self, page):
        base = (page - 1) * self.per_page
        return self.entries[base:base + self.per_page]

    def get_content(self, entries, page, *, first=False):
        return None

    def get_embed(self, entries, page, *, first=False, nums=True):
        self.prepare_embed(entries, page, first=first, nums=nums)
        return self.embed

    def prepare_embed(self, entries, page, *, first=False, nums=True):
        p = []
        if nums:
            for index, entry in enumerate(entries, 1 + ((page - 1) * self.per_page)):
                p.append(f"{index}. {entry}")
        else:
            for index, entry in enumerate(entries, 1 + ((page - 1) * self.per_page)):
                p.append(f"{entry}")

        if self.maximum_pages > 1:
            if self.show_entry_count:
                text = f"第 {page}/{self.maximum_pages} 頁"
            else:
                text = f"第 {page}/{self.maximum_pages} 頁"

            self.embed.set_footer(text=text)

        if self.paginating and first:
            p.append("")
            p.append("**看不懂？點擊 \N{INFORMATION SOURCE} 查看說明書**")

        self.embed.description = "\n".join(p)

    async def show_page(self, page, *, first=False, nums=True):
        nums = self.numsbool
        self.current_page = page
        entries = self.get_page(page)
        content = self.get_content(entries, page, first=first)
        embed = self.get_embed(entries, page, first=first, nums=nums)

        if not self.paginating:
            return await self.channel.send(content=content, embed=embed)

        if not first:
            await self.message.edit(content=content, embed=embed)
            return

        self.message = await self.channel.send(content=content, embed=embed)
        for (reaction, _) in self.reaction_emojis:
            if self.maximum_pages == 2 and reaction in ("\u23ed", "\u23ee"):
                continue

            await self.message.add_reaction(reaction)

    async def checked_show_page(self, page):
        if page != 0 and page <= self.maximum_pages:
            await self.show_page(page)

    async def first_page(self):
        """前往第一頁"""
        await self.show_page(1)

    async def last_page(self):
        """前往最後一頁"""
        await self.show_page(self.maximum_pages)

    async def next_page(self):
        """前往下一頁"""
        await self.checked_show_page(self.current_page + 1)

    async def previous_page(self):
        """前往上一頁"""
        await self.checked_show_page(self.current_page - 1)

    async def show_current_page(self):
        if self.paginating:
            await self.show_page(self.current_page)

    async def numbered_page(self):
        """輸入頁數並前往該頁數"""
        to_delete = []
        embed = discord.Embed(title="你想前往第幾頁呢？", colour=discord.Colour.gold())
        embed.set_footer(
            text=f"在聊天欄輸入頁數數字即可 | /help 指令"
        )
        to_delete.append(await self.channel.send(embed=embed))

        def message_check(m):
            return m.author == self.author and \
                self.channel == m.channel and \
                m.content.isdigit()

        try:
            msg = await self.bot.wait_for("message", check=message_check, timeout=30.0)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="因為訊息過於久遠，系統無法刪除訊息",
                colour=discord.Colour.red()
            )

            embed.set_footer(
                text=f"錯誤碼：80 | TimeoutError"
            )

            to_delete.append(await self.channel.send(embed))
            await asyncio.sleep(5)
        else:
            page = int(msg.content)
            to_delete.append(msg)
            if page != 0 and page <= self.maximum_pages:
                await self.show_page(page)
            else:
                embed = discord.Embed(
                    title="找不到該頁數！",
                    colour=discord.Colour.red()
                )

                embed.set_footer(
                    text=f"錯誤碼：85 | NotFoundError"
                )
                to_delete.append(await self.channel.send(embed=embed))
                await asyncio.sleep(2.5)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass

    async def show_help(self):
        """顯示這個訊息"""
        messages = ["🎉  歡迎使用 互動式介面\n"]
        messages.append("使用 互動式介面，你可以透過下面的 "
                        "Emoji 反應來切換介面。\n如下表所述：\n")

        for (emoji, func) in self.reaction_emojis:
            messages.append(f"{emoji} {func.__doc__}")

        embed = self.embed.copy()
        embed.clear_fields()
        embed.description = "\n".join(messages)
        embed.set_footer(text=f"你目前在第 {self.current_page} 頁。")
        await self.message.edit(content=None, embed=embed)

        async def go_back_to_current_page():
            await asyncio.sleep(60.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def stop_pages(self):
        """刪除此訊息"""
        await self.message.delete()
        self.paginating = False

    def react_check(self, reaction, user):
        if user is None or user.id != self.author.id:
            return False

        if reaction.message.id != self.message.id:
            return False

        for (emoji, func) in self.reaction_emojis:
            if reaction.emoji == emoji:
                self.match = func
                return True
        return False

    async def paginate(self):
        """Actually paginate the entries and run the interactive loop if necessary."""
        first_page = self.show_page(1, first=True)
        if not self.paginating:
            await first_page
        else:
            # allow us to react to reactions right away if we"re paginating
            self.bot.loop.create_task(first_page)

        while self.paginating:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=self.react_check, timeout=120.0)
            except asyncio.TimeoutError:
                self.paginating = False
                try:
                    await self.message.clear_reactions()
                except:
                    pass
                finally:
                    break

            try:
                await self.message.remove_reaction(reaction, user)
            except:
                pass  # can"t remove it so don"t bother doing so

            await self.match()
