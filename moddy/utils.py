import asyncio
import contextlib
import importlib
import time
from dataclasses import dataclass
from typing import Coroutine

import discord
from rich.console import Console


event_loop = asyncio.get_event_loop()
console = Console()
numbers = {"A": "1️⃣", "B": "2️⃣", "C": "3️⃣", "D": "4️⃣"}
languages = ["python", "javascript"]


def limit(string: str, limit: int):
    if len(string) > limit:
        return f"{string[:limit]}..."
    return string


def call_every(*, secs):
    def wrapper(coro: Coroutine):
        async def schedular(*args, **kwargs):
            while True:
                await coro(*args, **kwargs)
                await asyncio.sleep(secs)

        return schedular

    return wrapper


@dataclass
class Timer:
    elapsed: int = 0


@contextlib.contextmanager
def benchmark():
    timer = Timer()
    start = time.perf_counter()
    yield timer
    finish = time.perf_counter()
    timer.elapsed = round(finish - start, 2)


def get_mention(user: discord.Member):
    return f"[{user.color}]@{user.display_name}[/{user.color}]"


def remove_prefix(string, prefix):
    if string.startswith(prefix):
        string = string[len(prefix) :]
    return string


def reloadr(*modules):
    from moddy import embeds, utils

    modules = [embeds, utils, *modules]
    for module in modules:
        importlib.reload(module)
