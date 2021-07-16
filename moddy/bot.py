import importlib
import os

from discord.ext import commands

from moddy.utils import log


class DiscordBot(commands.Bot):
    def __init__(self, db, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or("."), **kwargs)
        self.db = db
        self.load_cogs()

    @property
    def cogs(self):
        cog_files = os.listdir("moddy/cogs/")
        cog_modules = [
            importlib.import_module(f"moddy.cogs.{cog_file.strip('.py')}")
            for cog_file in cog_files
            if cog_file.endswith(".py")
        ]
        glob_vals = []
        for module in cog_modules:
            glob_vals.extend(module.__dict__.values())

        for val in glob_vals:
            if isinstance(val, commands.CogMeta):
                yield val

    def load_cogs(self, *, reload=False):
        for cog in self.cogs:
            try:
                if reload:
                    self.remove_cog(cog.__name__)
                self.add_cog(cog(self))

            except Exception as exc:
                print(
                    f"Could not load extension {cog.__name__} due to {exc.__class__.__name__}: {exc}"
                )

    async def on_ready(self):
        log("Logged on as {0} (ID: {0.id})".format(self.user))
        self.is_connected = True

    async def on_disconnect(self):
        if self.is_connected:
            log("[red]Connection closed with discord websocket")
            self.is_connected = False
