# -*- coding: utf-8 -*-


import asyncio
from moddy.logger import logger

from discord.ext import commands
from discord.message import Message
from moddy.embeds import ModdyEmbed, command_not_allowed, ping_embed, reload_embed
from moddy.utils import benchmark, reloadr

reloadr()


class General(commands.Cog):
    """The description for General goes here."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name="clear")
    async def clear_messages(self, ctx: commands.Context, amount: int = 0):
        if ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.channel.purge(limit=amount + 1)

        else:
            await ctx.send(embed=command_not_allowed("clear", "Manage messages"))

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
        asyncio.create_task(message.delete())
        await ctx.send(embed=ping_embed(self.bot.latency, timer.elapsed))


def setup(bot):
    bot.add_cog(General(bot))
