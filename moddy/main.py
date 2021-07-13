
import aiohttp

from .bot import DiscordBot
from .database.db_utils import client
from .utils import event_loop, headers, share_data


class Moddity:
    def __init__(self, **kwargs) -> None:
        self.loop = event_loop
        self.bot = DiscordBot()
        self.bot.load_cogs()
        self.db = client
        self.http = aiohttp.ClientSession(headers=headers)
        share_data(self)

    async def start(self) -> None:
        try:
            self.bot.remove_command("help")
            self.loop.create_task(self.bot.start("X"))

        except Exception as e:
            print(repr(e))

        await self.bot.wait_until_ready()

    def close(self):
        self.bot.close()
        self.http.close()
        self.loop.close()

    def run(self) -> None:
        try:
            self.loop.run_until_complete(self.start())

        finally:
            self.close()


moddity = Moddity()


def main():
    moddity.run()
