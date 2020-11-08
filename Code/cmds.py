import discord
from Core.classes import Cog
from discord.ext import commands
from random import randint


class Cmds(Cog):    
    # member command
    @commands.command(name="ping", description="查看自身的網路延遲度 | /ping")
    async def ping(self, ctx):
        embed = discord.Embed(color=0x3939ff)

        embed.set_author(
            name=f"延遲時間：{round((self.bot.latency * 1000), 2)} 毫秒(ms)",
            icon_url="https://raw.githubusercontent.com/open3/openBot/master/res/ping.png"
        )

        embed.set_footer(
            text=f"由 {str(ctx.author)[:5]} 提起 | /ping 指令"
        )

        await ctx.send(embed=embed)

    @commands.command(name="dice", description="使用骰子進行亂數選擇 n(1) 次 | /dice [n(1)]")
    async def dice(self, ctx, time=1):
        embed = discord.Embed(color=0xeb4034)

        embed.set_footer(
            text=f"由 {str(ctx.author)[:5]} 提起 | /dice 指令"
        )

        for i in range(time):
            num = randint(1, 6)

            embed.set_author(
                name=f"你骰出了 {num}",
                icon_url=f"https://raw.githubusercontent.com/open3/openBot/master/res/dice{num}.png"
            )

            await ctx.send(embed=embed)

    @commands.command(name="bot", description="查看 openBot GitHub 原始碼 | /bot")
    async def bot(self, ctx):
        embed = discord.Embed(description="https://github.com/open3studio/openBot\n",
                              colour=0xa527e8
                              )

        embed.set_thumbnail(
            url="https://raw.githubusercontent.com/open3/openBot/master/res/bot.png")

        embed.set_author(
            name="openBot GitHub 原始碼",
            icon_url="https://raw.githubusercontent.com/open3/openBot/master/res/logo/logo.png"
        )

        embed.set_footer(
            text=f"版本：{self.botver} | /bot 指令"
        )

        await ctx.send(embed=embed)

    # administrator command
    @commands.command(name="echo", description="使用 openBot 傳送訊息 | /echo [內容]")
    async def echo(self, ctx, *msg):
        if ctx.message.author.guild_permissions.administrator:
            if str(msg) == "()":
                await ctx.send(embed=self.send_error(ctx, "03"))
            else:
                await ctx.message.delete()
                await ctx.send(" ".join(msg))


def setup(bot):
    bot.add_cog(Cmds(bot))
