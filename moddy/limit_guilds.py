import functools
from moddy.bot import DiscordBot
from typing import Any, Callable, List, Type, TypeVar

from discord import Message
from discord.ext import commands

from moddy.logger import logger

deco = TypeVar("deco", bound=Callable[..., Any])


class limitedguilds(commands.Cog):
    cmds: List[commands.Command] = []
    listeners: List[Callable]

    def __init__(self, bot) -> None:
        self.bot: DiscordBot = bot

    @property
    def guild_id(self) -> int:
        return 0

    @staticmethod
    def command(*args, **kwargs):  # type: ignore
        def wrapper(func: deco):
            @functools.wraps(func)
            async def comm(self, ctx: commands.Context, *args, **kwargs):
                guild_id = self.guild_id  # type: ignore
                guild = self.bot.get_guild(guild_id)
                if guild != ctx.guild:
                    return
                return await func(self, ctx, *args, **kwargs)

            return commands.command(*args, **kwargs)(comm)

        return wrapper

    @staticmethod
    def listener(name=""):  # type: ignore
        def wrapper(func: deco):
            @functools.wraps(func)
            async def comm(self: Type[limitedguilds], arg1: Any, *args, **kwargs):
                guild_id = self.guild_id  # type: ignore
                required_guild = self.bot.get_guild(guild_id)

                if isinstance(arg1, Message):
                    guild = arg1.guild
                if required_guild != guild:
                    return
                return await func(self, arg1, *args, **kwargs)

            return commands.Cog.listener(name=name)(comm)

        return wrapper
