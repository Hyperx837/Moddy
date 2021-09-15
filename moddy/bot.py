from asyncio.tasks import Task
import os
from pathlib import Path
from typing import List

import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded
from discord.flags import Intents

import moddy.main
from moddy.logger import logger


class DiscordBot(commands.Bot):
    def __init__(self, main, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or("."),
            intents=Intents.all(),
            **kwargs,
        )
        self.main = main
        self.db = main.db
        self.session = main.http
        self.is_connected = False
        self.cog_paths = [*main.config.cog_paths, "cogs/"]
        self.last_deleted = None
        self.tasks: List[Task] = []
        self.load_cogs()

    @property
    def cog_names(self):
        for cog_path in self.cog_paths:
            path = self.main.base / Path(cog_path)
            for file in path.glob("*.py"):
                if file.name.startswith("__"):
                    continue

                module_name = str(path / file.stem).replace("/", ".")
                yield module_name

    def load_cogs(self, *, reload=False):
        loader = self.reload_extension if reload else self.load_extension
        for cog in self.cog_names:
            try:
                loader(cog)

            except ExtensionAlreadyLoaded:
                self.load_extension(cog)  # detect new cogs while reloading
                logger.success(f"Successfully loaded {cog}")

            except Exception as exc:
                logger.error(
                    f"Could not load extension {cog} due to {exc.__class__.__name__}: {exc}"
                )

    async def on_ready(self):
        logger.log("Logged on as {0} (ID: {0.id})".format(self.user))
        activity = discord.Game("with Reality")
        await self.change_presence(status=discord.Status.idle, activity=activity)
        self.is_connected = True

    async def on_disconnect(self):
        if self.is_connected:
            logger.error("Connection closed with discord websocket")
            self.is_connected = False
