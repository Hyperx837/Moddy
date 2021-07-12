import importlib
from typing import Callable, Union

import aiohttp
from aiohttp import ClientResponse
from rich.console import Console

log: Callable = Console().log


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


def reloadr():
    from moddy import embeds, utils

    importlib.reload(utils)
    importlib.reload(embeds)


async def get_url(
    url, *args, json=False, text=False, **kwargs
) -> Union[ClientResponse, dict, str]:
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, *args, **kwargs) as response:
            if json:
                return await response.json()

            elif text:
                return await response.text()

            return response


numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
