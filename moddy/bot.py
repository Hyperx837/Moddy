#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib

from discord.ext import commands

from moddy import config
# from moddy.config import cogs, api_tokens
from moddy.utils import log

# if config.


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or("."), **kwargs)
        self.load_cogs()

    def load_cogs(self, *, reload=False):
        importlib.reload(config)
        for cog in config.cogs:
            extention = f"moddy.cogs.{cog}"
            try:
                if reload:
                    self.reload_extension(extention)
                else:
                    self.load_extension(extention)
            except Exception as exc:
                print(
                    "Could not load extension {0} due to {1.__class__.__name__}: {1}".format(
                        cog, exc
                    )
                )

    async def on_ready(self):
        log("Logged on as {0} (ID: {0.id})".format(self.user))
        self.is_connected = True

    async def on_disconnect(self):
        if self.is_connected:
            log("[red]Connection closed with discord websocket")
            self.is_connected = False


# write general commands here


def main():
    bot = Bot()
    bot.run(config.api_tokens["discord"])
