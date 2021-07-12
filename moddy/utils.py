from typing import Callable, Union

import aiohttp
from aiohttp import ClientResponse
from rich.console import Console

log = Console().log


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
