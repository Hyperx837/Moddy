import os

from discord.ext import commands
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
        cog_files = os.listdir("moddy/cogs/")
        for file in cog_files:
            if file.endswith(".py") and not file.startswith("__"):
                yield f"moddy.cogs.{file.strip('.py')}"
        # cog_modules = (
        #     importlib.import_module(f"moddy.cogs.{cog_file.strip('.py')}")
        #     for cog_file in cog_files
        #     if cog_file.endswith(".py")
        #  )
        # glob_vals = []
        # for module in cog_modules:
        #     glob_vals.extend(module.__dict__.values())

        # for val in glob_vals:
        #     if isinstance(val, commands.CogMeta):
        #         yield val

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
