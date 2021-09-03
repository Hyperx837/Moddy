import functools
from typing import Any, Callable, List, TypeVar

from discord.ext import commands

import moddy.main
from moddy.logger import logger

deco = TypeVar("deco", bound=Callable[..., Any])


class LimitedGuilds(commands.Cog):
    cmds: List[commands.Command] = []

    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @classmethod
    def command(cls, *args, **kwargs):  # type: ignore
        def wrapper(func: deco):
            @functools.wraps(func)
            async def comm(self, ctx: commands.Context, *args, **kwargs):
                guild_id = func.__self__.guild_id  # type: ignore
                guild = moddy.main.moddity.bot.get_guild(guild_id)
                if guild != ctx.guild:
                    return
                return await func(self, ctx, *args, **kwargs)

            return commands.command(*args, **kwargs)(comm)

        return wrapper

    # def __getattribute__(self, name: str):
    #     value = super().__getattribute__(name)
    #     if isinstance(value, tuple):
    #         guild_id = super().__getattr__("guild_id")
    #         attr_val = tuple(
    #             # commands.Command.__call__

    #             for func in value
    #             if isinstance(func, commands.Command)
    #         )
    #         return attr_val

    #     return value
