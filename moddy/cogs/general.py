# -*- coding: utf-8 -*-
import asyncio

from discord.ext import commands
from moddy.embeds import command_not_allowed
from moddy.utils import log


class General(commands.Cog):
    """The description for General goes here."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name="clear")
    async def clear_messages(self, ctx: commands.Context, amount: int = 0):
        if ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.channel.purge(limit=amount)

        else:
            await ctx.send(embed=command_not_allowed("clear", "Manage messages"))

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload_cogs(self, *_):
        self.bot.load_cogs(mode="reload")
        log("[bold green]Cogs successfully reloaded")


def setup(bot):
    bot.add_cog(General(bot))
