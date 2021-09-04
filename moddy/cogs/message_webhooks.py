# -*- coding: utf-8 -*-
from typing import Tuple

import discord
from discord.ext import commands
from moddy.config import my_guild
from moddy.limit_guilds import limitedguilds
from moddy.logger import logger
from moddy.utils import send_hook


class MessageWebhooks(limitedguilds):
    """The description for Developer goes here."""

    @commands.command(name="replicater")
    async def send_webhook(self, ctx: commands.Context, user: discord.Member, *words):
        message = " ".join(words)
        if ctx.guild.id != my_guild:
            return

        if not ctx.author.permissions_in(ctx.channel).manage_webhooks:
            return

        await send_hook("Hooker", ctx.channel, message, user=user)


def setup(bot):
    bot.add_cog(MessageWebhooks(bot))
