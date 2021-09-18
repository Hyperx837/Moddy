# -*- coding: utf-8 -*-
from typing import Tuple

import discord
from discord.errors import Forbidden
from discord.ext import commands
from moddy.logger import logger
from moddy.utils.discord import send_hook


class MessageWebhooks(commands.Cog):
    """The description for Developer goes here."""

    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name="replicater")
    async def send_webhook(self, ctx: commands.Context, user: discord.Member, *words):
        message = " ".join(words)
        # if not self.bot.user.permissions_in(ctx.channel).manage_webhooks:

        if (
            not ctx.author.permissions_in(ctx.channel).manage_webhooks
            and not self.bot.owner_id == ctx.author.id
        ):
            await ctx.send("You don't have manage webhooks permission")
            return

        try:
            await send_hook("Mod Hook", ctx.channel, message, user=user)

        except Forbidden:
            await ctx.send("I don't have manage webhooks permission")
            await ctx.send(":cry:")


def setup(bot):
    bot.add_cog(MessageWebhooks(bot))
