import functools
from typing import Callable

import moddy.main
from discord.ext import commands


def guild_only(*, cmd_func=None, command_name: str, guild_id: int):
    def wrapper(func: Callable):
        @functools.wraps(func)
        async def command(ctx: commands.Context, *args, **kwargs):
            guild = moddy.main.moddity.bot.get_guild(guild_id)
            if guild != ctx.guild:
                return
            return await func(ctx, *args, **kwargs)

        # if cmd_func:
        #     return command
        return commands.command(name=command_name)(command)

    return wrapper(cmd_func) if cmd_func else wrapper
