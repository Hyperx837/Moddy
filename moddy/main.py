import asyncio
import sys
from aiohttp import ClientSession

from .bot import DiscordBot
from .config import api_tokens
from .database.database import database
from .logger import logger

# from .proxy import Session


class Moddity:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.db = database
        # self.http = Session()
        self.http = ClientSession()
        self.bot = DiscordBot(self.db, self.http)
        self.discordbot_token = api_tokens["discord"]

    async def start(self) -> None:
        self.loop.create_task(self.bot.start(self.discordbot_token))
        await self.bot.wait_until_ready()
        # asyncio.create_task(self.http.renew_proxy())

    async def close(self):
        await self.bot.close()
        # await self.http.close()
        pending = asyncio.all_tasks()
        await asyncio.gather(*pending)
        self.loop.close()

    def run(self) -> None:
        try:
            self.loop.run_until_complete(self.start())
            self.loop.run_forever()

        except KeyboardInterrupt:
            self.loop.create_task(self.close())
            sys.stdout.write("\b\b")
            logger.log("[bold cyan]Exiting... ")


moddity = Moddity()


def main():
    moddity.run()
