import asyncio
from dataclasses import dataclass
from typing import Optional, Union

from aiohttp import ClientResponse, ClientSession
from bs4 import BeautifulSoup

from .database.database import database
from .logger import logger
from .utils.misc import call_every


class Session:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.proxy_coll = database["proxy"]
        self.proxy: Proxy = {}
        self.proxy_url: str = ""
        self.session = ClientSession()

    @call_every(secs=300)
    async def renew_proxy(self):
        result = await self.get_url("https://free-proxy-list.net", text=True)
        soup = BeautifulSoup(result, "lxml")
        proxy = list(soup.select_one("tbody tr").children)
        ip, port, country, is_https = [proxy[n].text for n in (0, 1, 3, 6)]
        if is_https == "yes":
            protocol = "https"
        else:
            protocol = "http"
        self.proxy = Proxy(ip, port, protocol, country)
        self.proxy_url = f"{protocol}://{ip}:{port}"
        logger.info(
            f"Connected to [blue u]{self.proxy_url}\n[/]"
            f"[#8af9ff]Location[/]: [#c76eff]{self.proxy.country}"
        )

    async def get_url(
        self, url, *args, json=False, text=False, **kwargs
    ) -> Union[ClientResponse, dict, str]:
        async with self.session.get(  # type: ignore
            url, headers=self.headers, proxy=self.proxy_url, *args, **kwargs
        ) as response:
            if json:
                return await response.json()

            elif text:
                return await response.text()

            return response

    async def close(self):
        await self.session.close()


@dataclass
class Proxy:
    ip: str
    port: str
    protocol: str
    country: str
