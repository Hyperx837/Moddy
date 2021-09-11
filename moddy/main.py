import asyncio
import sys
from typing import Type, Union

from aiohttp import ClientSession

from .bot import DiscordBot
from .config import api_tokens
from .database.database import database
from .logger import logger

# from .proxy import Session


class Moddity:
    def __init__(self, config) -> None:
        self.loop = asyncio.get_event_loop()
        self.db = database
        # self.http = Session()
        self.http = ClientSession()
        self.config = config
        self.bot = DiscordBot(self)

    async def start(self) -> None:
        self.loop.create_task(self.bot.start(self.config.token))  # type: ignore
        await self.bot.wait_until_ready()

    async def close(self):
        await self.bot.close()
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


moddity = None


def main(config):
    global moddity
    moddity = Moddity(config)
    moddity.run()
