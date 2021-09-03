import os

from discord.ext import commands
from .config import cog_paths
from discord.ext.commands.errors import ExtensionAlreadyLoaded

from .logger import logger


class DiscordBot(commands.Bot):
    def __init__(self, db, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or("."), **kwargs)
        self.db = db
        self.is_connected = False
        self.load_cogs()

    @property
    def cogs(self):
        for path in cog_paths:
            cog_files = os.listdir(f"moddy/cogs/{path}")
            for file in cog_files:
                if file.endswith(".py") and not file.startswith("__"):
                    yield f"moddy.cogs.{path.replace('/', '.')}{file.strip('.py')}"

    def load_cogs(self, *, reload=False):
        loader = self.reload_extension if reload else self.load_extension
        for cog in self.cogs:
            try:
                loader(cog)

            except ExtensionAlreadyLoaded:
                self.load_extension(cog)  # detect new cogs while reloading

            except Exception as exc:
                print(
                    f"Could not load extension {cog} due to {exc.__class__.__name__}: {exc}"
                )

    async def on_ready(self):
        logger.log("Logged on as {0} (ID: {0.id})".format(self.user))
        self.is_connected = True

    async def on_disconnect(self):
        if self.is_connected:
            logger.error("Connection closed with discord websocket")
            self.is_connected = False
