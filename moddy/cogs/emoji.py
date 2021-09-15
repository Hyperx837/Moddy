# -*- coding: utf-8 -*-
from moddy.embeds import ModdyEmbed

import discord
import moddy.bot
from discord import message
from discord.ext import commands


class Emoji(commands.Cog):
    """The description for Developer goes here."""

    def __init__(self, bot: moddy.bot.DiscordBot):
        self.bot = bot

    @commands.command(name="add-emoji")
    async def add_emoji(self, ctx: commands.Context, name: str):
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(msg.attachments) == 0:
            await ctx.send("Please provide an image")
            return
        for attach in msg.attachments:
            image = await attach.read()
            await ctx.guild.create_custom_emoji(name=name, image=image)
            await ctx.send(f"added emoji {name}")

    @commands.command(name="rename-emoji")
    async def rename_emoji(self, ctx: commands.Context, oldname: str, newname: str):
        pass


def setup(bot):
    bot.add_cog(Emoji(bot))
