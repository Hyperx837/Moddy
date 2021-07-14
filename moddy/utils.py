import asyncio
import importlib
from typing import Union

import discord
from aiohttp import ClientResponse
from rich.console import Console

import moddy.main

event_loop = asyncio.get_event_loop()
console = Console()
numbers = {"A": "1️⃣", "B": "2️⃣", "C": "3️⃣", "D": "4️⃣"}
languages = ["python", "javascript"]
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
session = moddy.main.moddity.http


def log(*args, **kwargs):
    console.log(*args, **kwargs)


def get_mention(user: discord.Member):
    return f"[{user.color}]@{user.display_name}[/{user.color}]"


def remove_prefix(string, prefix):
    if string.startswith(prefix):
        string = string[len(prefix) :]
    return string


def reloadr():
    from moddy import embeds, utils

    importlib.reload(utils)
    importlib.reload(embeds)


async def get_url(
    url, *args, json=False, text=False, **kwargs
) -> Union[ClientResponse, dict, str]:
    print(url)
    async with session.get(url, headers=headers, *args, **kwargs) as response:
        if json:
            return await response.json()

        elif text:
            return await response.text()

        return response
