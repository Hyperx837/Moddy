#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

from .config import cogs, discordbot_token


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or("$"), **kwargs)
        for cog in cogs:
            try:
                self.load_extension(f"moddy.cogs.{cog}")
            except Exception as exc:
                print(
                    "Could not load extension {0} due to {1.__class__.__name__}: {1}".format(
                        cog, exc
                    )
                )

    async def on_ready(self):
        print("Logged on as {0} (ID: {0.id})".format(self.user))
        self.is_connected = True

    async def on_disconnect(self):
        if self.is_connected:
            print("Connection closed with discord websocket")
            self.is_connected = False


bot = Bot()
# write general commands here


def main():
    bot.run(discordbot_token)
