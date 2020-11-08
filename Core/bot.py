import discord
import os
from discord.ext import commands
from Core.classes import Data
from Core.menu import Pages


class PaginatedHelpCommand(commands.HelpCommand):
    async def PaginateMenu(self, entries, per_page=10, show_entry_count=True, numsbool=True, embedcolor='blurple', thumbnail=None):
        PMenuConsole = Pages(self.context, entries=entries, per_page=per_page,
                             show_entry_count=show_entry_count, numsbool=numsbool, embedcolor=embedcolor, thumbnail=thumbnail)
        await PMenuConsole.paginate()

    async def send_bot_help(self, mapping):
        messages = ["**openBot 可使用的指令**", "",
                    "\n📙    `/help`\n", "查閱指令指南",
                    "\n🎲    `/dice [n]`\n", "使用骰子進行亂數選擇 n(1) 次",
                    "\n🌐   `/ping`\n", "查看自身的網路延遲度",
                    "\n🤖    `/bot`\n", "查看 openBot GitHub 原始碼",
                    "\n**僅供管理員可使用的指令**", "",
                    "\n🤖    `/echo`\n", "使用 openBot 傳送訊息", ]
        await self.PaginateMenu(entries=messages, numsbool=False, embedcolor='orange', thumbnail="https://raw.githubusercontent.com/open3/OpenBot/master/Res/report.png")

    async def send_command_help(self, command):
        messagess = []
        descbool = True
        helpbool = True
        if command.description:
            descbool = True
        else:
            descbool = False
        if command.help:
            helpbool = True
        else:
            helpbool = False

        if descbool and helpbool:
            messagess.append(f'{command.description}\n\n{command.help}')
        elif descbool:
            messagess.append(f'{command.description}')
        elif helpbool:
            messagess.append(f'{command.help}')
        await self.PaginateMenu(entries=messagess, numsbool=False, embedcolor='orange')

    async def command_not_found(self, string):
        embed = discord.Embed(
            title="沒有這個指令。查看可用指令請使用 /help",
            colour=discord.Colour.red()
        )

        embed.set_footer(
            text=f"錯誤碼：01 | CommandNotFoundError"
        )

        await self.context.send(embed=embed)
        return


class Bot(Data):
    def run(self, token):
        bot = commands.Bot(command_prefix='/',
                           help_command=PaginatedHelpCommand())

        @bot.command()
        async def reload(ctx):
            for fn in os.listdir("./Code"):
                if fn.endswith(".py"):
                    bot.reload_extension(f"Code.{fn[:-3]}")

        for fn in os.listdir("./Code"):
            if fn.endswith(".py"):
                bot.load_extension(f"Code.{fn[:-3]}")

        bot.run(token)
