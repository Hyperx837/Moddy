from .bot import DiscordBot
from .database.database import database
from .utils import event_loop, session
from .config import api_tokens


class Moddity:
    def __init__(self) -> None:
        self.loop = event_loop
        self.db = database
        self.http = session
        self.bot = DiscordBot(self.db)
        self.discordbot_token = api_tokens["discord"]

    async def start(self) -> None:
        try:
            self.bot.remove_command("help")
            self.loop.create_task(self.bot.start(self.discordbot_token))

        except Exception as e:
            print(repr(e))

        await self.bot.wait_until_ready()

    async def close(self):
        await self.bot.close()
        await self.http.close()
        self.loop.close()

    def run(self) -> None:
        try:
            self.loop.run_until_complete(self.start())
            self.loop.run_forever()

        except KeyboardInterrupt:
            self.loop.create_task(self.close())


moddity = Moddity()


def main():
    moddity.run()
