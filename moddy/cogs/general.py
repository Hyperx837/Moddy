# -*- coding: utf-8 -*-
from moddy.utils import log
from discord.ext import commands
import discord

class General(commands.Cog):
    """The description for General goes here."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx: commands.Context, amount: int = 0):
        await ctx.channel.purge(limit=amount)
    
    @commands.command(name="reload")
    @commands.is_owner()
    async def reload_cogs(self, *_):
        self.bot.load_cogs(mode="reload")
        log("[bold green]Cogs successfully reloaded")


def setup(bot):
    bot.add_cog(General(bot))
