# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from moddy.utils import ModdyMessage, get_quiz, parse_data


class Quiz(commands.Cog):
    """The description for Quiz goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="quiz")
    async def send_quiz(self, ctx: commands.Context):
        json_data = await get_quiz()
        question, answers = parse_data(json_data)
        await ctx.send(embed=ModdyMessage(question, answers))
        # ctx.send()


def setup(bot):
    bot.add_cog(Quiz(bot))
