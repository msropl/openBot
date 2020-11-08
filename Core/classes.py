import discord
import json
import requests
from discord.ext import commands


class Data():
    def __init__(self):
        with open("./Data/zh-tw/error_code.json", "r", encoding="utf8") as jfile:
            self.error_code = json.load(jfile)
        with open("./Data/info.json", "r", encoding="utf8") as jfile:
            self.botinfo = json.load(jfile)
        with open("./Data/token", "r", encoding="utf8") as jfile:
            self.bottoken = jfile.read()
        self.botver = self.botinfo["VERSION"]
        self.botreq = self.botinfo["REQUIREMENTS"]
        self.a = requests.get(
            "https://raw.githubusercontent.com/open3/openBot/master/preview.txt")


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("./Data/zh-tw/error_code.json", "r", encoding="utf8") as jfile:
            self.error_code = json.load(jfile)
        with open("./Data/info.json", "r", encoding="utf8") as jfile:
            self.botinfo = json.load(jfile)
        with open("./Data/setting.json", "r", encoding="utf8") as jfile:
            self.setting = json.load(jfile)
        self.botver = self.botinfo["VERSION"]
        self.botreq = self.botinfo["REQUIREMENTS"]
        self.server_id = self.setting["SERVER_ID"]
        self.role_vote = self.setting["ROLE_VOTE"]
        self.a = requests.get(
            "https://raw.githubusercontent.com/open3/openBot/master/preview.txt")

    def send_error(self, ctx, code):
        with open("./Data/zh-tw/error_code.json", "r", encoding="utf8") as jfile:
            error_code = json.load(jfile)
        title = error_code[code]
        embed = discord.Embed(
            title=title,
            colour=discord.Colour.red()
        )
        embed.set_footer(
            text=error_code[code + "foot"]
        )
        return embed
