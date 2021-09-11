# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from moddy.logger import logger
from moddy.utils import get_url


class Dictionary(commands.Cog):
    """The description for Developer goes here."""

    def __init__(self, bot):
        self.base_url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/{}"
        self.bot = bot

    @commands.command(name="dict")
    async def dictionary(self, ctx: commands.Context, *words):
        phrase = " ".join(words)
        url = self.base_url.format(phrase)
        resp = await get_url(url, json=True)
        try:
            meaning = resp[0]["meanings"][0]["definitions"][0]["definition"]
            await ctx.send(meaning)

        except (IndexError, KeyError):
            await ctx.send("you'll get the nobel price for inventing words")


def setup(bot):
    bot.add_cog(Dictionary(bot))
