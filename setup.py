import discord
from Core.bot import Bot


class Setup(Bot):
    def initial(self):
        pass

    def boot(self):
        print(f"[資訊] Discord.py：{discord.__version__}")
        print(f"[資訊] openBot   ：{self.botver}")

        self.run(self.bottoken)


if __name__ == "__main__":
    setup = Setup()
    setup.boot()
