import asyncio
import importlib  # noqa: F401
from inspect import iscoroutine

import discord
import moddy.bot
import moddy.main  # noqa: F401
from discord.ext import commands


class Eval(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: moddy.bot.DiscordBot = bot
        self.task = asyncio.create_task

    @commands.command("exec")
    @commands.is_owner()
    async def exec(self, ctx, *expression):
        out = exec(" ".join(expression))
        if iscoroutine(out):
            await out

    @commands.command("eval")
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, expression: str):
        try:
            output = eval(expression)

        except Exception as exc:
            output = f"`Error: {exc}`"

        await ctx.send(output)

    def evaluater(self, expression):
        if "=" in expression:
            lhs, rhs = expression.split(" = ")
            globals[lhs] = rhs


def setup(bot):
    bot.add_cog(Eval(bot))
