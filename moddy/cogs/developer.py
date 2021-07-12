# -*- coding: utf-8 -*-

from discord.ext import commands


class Developer(commands.Cog):
    """The description for Developer goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command("stars")
    async def get_stargazers(self, ctx: commands.Context, repo: str):
        chart_url = f"https://starchart.cc/{repo}.svg"
        await ctx.send(chart_url)


def setup(bot):
    bot.add_cog(Developer(bot))
