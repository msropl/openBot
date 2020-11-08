import discord
from Core.classes import Cog
from discord.ext import commands


class Event(Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[系統] 機器人已上線！\n[系統] 登入名稱：{self.bot.user}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=self.send_error(ctx, "01"))
        else:
            await ctx.send(embed=self.send_error(ctx, "99"))


def setup(bot):
    bot.add_cog(Event(bot))
