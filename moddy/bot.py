import os

import discord
from aiohttp.client import ClientSession
from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded
from discord.flags import Intents

from .logger import logger


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
        self.cog_paths = [*main.config.cog_paths, *main.config.common.cog_paths]
        self.last_deleted = None
        self.load_cogs()

    @property
    def cogs(self):
        for path in self.cog_paths:
            cog_files = os.listdir(f"moddy/cogs/{path}")
            for file in cog_files:
                if file.endswith(".py") and not file.startswith("__"):
                    filename, _ = os.path.splitext(file)
                    module = f"moddy.cogs.{path.replace('/', '.')}{filename}"
                    yield module

    def load_cogs(self, *, reload=False):
        loader = self.reload_extension if reload else self.load_extension
        for cog in self.cogs:
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
