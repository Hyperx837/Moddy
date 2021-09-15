import asyncio
import importlib
import sys
from pathlib import Path

from aiohttp import ClientSession

from .database.database import database
from .logger import logger

# from .proxy import Session


class Assembler:
    """puts everything together and provides methods to run the complete program"""

    def __init__(self, config) -> None:
        self.loop = asyncio.get_event_loop()
        self.db = database
        # self.http = Session()
        self.http = ClientSession()
        self.config = config
        bot_module = importlib.import_module(self.config.entrypoint)
        self.base = Path("moddy/")
        self.bot = bot_module.DiscordBot(self)  # type: ignore

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
            [self.loop.create_task(task) for task in self.bot.tasks]
            self.loop.run_forever()

        except KeyboardInterrupt:
            self.loop.create_task(self.close())
            sys.stdout.write("\b\b")
            logger.log("[bold cyan]Exiting... ")


assemble = None


def main(config):
    global assemble
    assemble = Assembler(config)
    assemble.run()
