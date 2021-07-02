#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from moddy.utils import log

from moddy.config import cogs, discordbot_token


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or("$"), **kwargs)
        self.load_cogs()

    def load_cogs(self, *, mode="load"):
        for cog in cogs:
            extention = f"moddy.cogs.{cog}"
            try:
                if mode == "reload":
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

    async def on_message(self, message: discord.Message):
        if message.content == "m.restart" and self.is_owner(message.author):
            self.load_cogs(mode="reload")
            log("[bold green]Cogs successfully reloaded")
        return await super().on_message(message)


bot = Bot()
# write general commands here


def main():
    bot.run(discordbot_token)
