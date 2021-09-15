import asyncio
import contextlib
import importlib
import os
import time
from dataclasses import dataclass
from typing import Coroutine, Union

import moddy.main
from aiohttp import ClientResponse
from rich.console import Console


class SecretNotFound(Exception):
    def __init__(self, secret, *args: object) -> None:
        error = f'Secret "{secret}" not found in either environment or config '
        super().__init__(error, *args)


def get_secret(secret: str) -> str:
    config = moddy.main.assemble.config
    env = os.getenv(secret) or os.getenv(secret.capitalize())
    if env:
        return env

    if hasattr(config, secret):
        return getattr(config, secret)

    raise SecretNotFound(secret)


headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
event_loop = asyncio.get_event_loop()
console = Console()
numbers = {"A": "1️⃣", "B": "2️⃣", "C": "3️⃣", "D": "4️⃣"}
languages = ["python", "javascript"]


def limit(string: str, limit: int):
    if len(string) > limit:
        return f"{string[:limit]}..."
    return string


def call_every(*, days=0, hours=0, minutes=0, secs=0):
    def wrapper(coro: Coroutine):
        async def schedular(*args, **kwargs):
            amount = days * 86400 + hours * 3600 + minutes * 60 + secs
            while True:
                await coro(*args, **kwargs)
                await asyncio.sleep(amount)

        return schedular

    return wrapper


async def request_url(
    url, *args, is_json=False, is_text=False, method="GET", **kwargs
) -> Union[ClientResponse, dict, str]:
    session = moddy.main.assemble.http
    if "headers" in kwargs:
        headers = kwargs.pop("headers")
    else:
        headers = globals()["headers"]
    async with session.request(  # type: ignore
        method, url, headers=headers, *args, **kwargs
    ) as response:
        if is_json:
            return await response.json()

        elif is_text:
            return await response.text()
        return response


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


def remove_prefix(string, prefix):
    if string.startswith(prefix):
        string = string[len(prefix) :]
    return string


def reloadr(*modules):
    from moddy import embeds
    from moddy.utils import discord, db, misc

    modules = [embeds, discord, db, misc, *modules]
    for module in modules:
        importlib.reload(module)
