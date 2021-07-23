import asyncio
import sys

import aiohttp

from .bot import DiscordBot
from .config import api_tokens
from .database.database import database
from .utils import console


class Moddity:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.db = database
        self.http = aiohttp.ClientSession()
        self.bot = DiscordBot(self.db)
        self.discordbot_token = api_tokens["discord"]

    async def start(self) -> None:
        self.loop.create_task(self.bot.start(self.discordbot_token))
        await self.bot.wait_until_ready()

    async def close(self):
        await self.bot.close()
        await self.http.close()
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
            console.log("[bold cyan]Exiting... ")


moddity = Moddity()


def main():
    moddity.run()
