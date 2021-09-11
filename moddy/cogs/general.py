# -*- coding: utf-8 -*-
import asyncio
import re
import traceback

import discord
from discord import Member, Message
from discord.ext import commands
from discord.role import Role
from moddy.config import deleted_channel
from moddy.embeds import (
    ModdyEmbed,
    ModdyError,
    command_not_allowed,
    ping_embed,
    reload_embed,
)
from moddy.logger import logger
from moddy.utils import benchmark, reloadr

reloadr()


class General(commands.Cog):
    """The description for General goes here."""

    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name="clear")
    async def clear_messages(self, ctx: commands.Context, amount: int = 0):
        chan = self.bot.get_channel(deleted_channel)
        if ctx.channel == chan and ctx.author.id != self.bot.owner_id:
            return
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send(embed=command_not_allowed("clear", "Manage messages"))
            return

        try:
            await ctx.message.delete()
            self.bot.last_deleted = ctx.message

        except discord.errors.NotFound:
            pass

        await ctx.channel.purge(limit=amount)
        message = await ctx.send(
            embed=ModdyEmbed(
                "I cleared up some junk",
                f"Cleared up {amount} message(s) requested to delete by `@{ctx.author.display_name}`",
            )
        )
        await message.delete(delay=5)
        self.bot.last_deleted = ctx.message

    @commands.command(name="reload")
    async def reload_cogs(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            self.bot.load_cogs(reload=True)
            await ctx.send(embed=reload_embed)
            logger.success("[bold green]Cogs successfully reloaded")

        else:
            await ctx.send(
                embed=ModdyEmbed(
                    "Please don't embarass your self",
                    "this command is limited to my owner",
                )
            )

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        with benchmark() as timer:
            message: Message = await ctx.send("Testing Ping...")
        await message.delete()
        await ctx.send(embed=ping_embed(self.bot.latency, timer.elapsed))


def setup(bot):
    bot.add_cog(General(bot))
