# -*- coding: utf-8 -*-

import gidgethub
import moddy.bot
from discord.ext import commands
from gidgethub.aiohttp import GitHubAPI


class GitHub(commands.Cog):
    """The description for Developer goes here."""

    def __init__(self, bot):
        self.bot: moddy.bot.DiscordBot = bot
        self.chart_url = "https://starchart.cc/{}.svg"

    @commands.command("stars")
    async def get_stargazers(self, ctx: commands.Context, repo: str):
        await ctx.send(self.chart_url.format(repo))

    @commands.command(name="repo")
    async def get_repo_data(self, ctx: commands.Context, repo: str):
        gh = GitHubAPI(
            self.bot.session,
            self.bot.main.config.common.gh_username,
            oauth_token=self.bot.main.config.common.tokens.gh,
        )
        try:
            repo_metadata = await gh.getitem(f"/repos/{repo}")
        except gidgethub.BadRequest:
            await ctx.send("Finding the closest match...")
            repos = (await gh.getitem(f"/search/repositories?q={repo}"))["items"]
            if len(repos) == 0:
                await ctx.send("such repo doesn't exist")
                return
            repo_metadata = repos[0]
        await ctx.send(repo_metadata["full_name"])


def setup(bot):
    bot.add_cog(GitHub(bot))
