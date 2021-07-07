# -*- coding: utf-8 -*-

from typing import Tuple

import discord
from bs4 import BeautifulSoup, Tag
from discord.ext import commands
from moddy.embeds import ModdyEmbed, google_embed
from moddy.utils import get_url


class Google(commands.Cog):
    """The description for Google goes here."""

    def __init__(self, bot):
        self.bot = bot

    def scrape_data(self, data) -> Tuple[str, str, str]:  # type: ignore[return]
        soup = BeautifulSoup(data, "lxml")
        answer_selectors = {
            ".XDTKBd": None,  # main result
            "div.wDYxhc:nth-child(2) > div > span > span": "",
            # "": "",
            ".kno-rdesc > span:nth-child(2)": None,  # sidebar result
            "div.VwiC3b > span:last-child": "div.g > div > div > div > a",  # main paragraph
            ".eKjLze > div > div > div > div:nth-child(2) > div > span": ".eKjLze > div > div > div > div > a",  # sometimes first search result somehow
            "div.hlcw0c > div> div:nth-child(2) > div > div > div > span:last-child": None,  # wikipedia result
            # "#rso > div > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > span": "",
            "#rso > div > div:nth-child(2) > div > div > div > span": "#rso > div > div:nth-child(2) > div > div > a",  # normal search results
            "div.hlcw0c:nth-child(3) > div > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > span": None,
            "div.hlcw0c:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)": None,
            # ".g > div > div > div:nth-child(2) > span > span:last-child": None,
            # "#rso > div > div > div > div:nth-child(2) > div > span"
        }
        for ans_selector, link_selector in answer_selectors.items():
            answer: Tag = soup.select_one(ans_selector)
            if answer and answer.text not in ("", "·", None):
                link: str = (
                    f'[Read More....]({soup.select_one(link_selector)["href"]})'
                    if link_selector
                    else ""
                )
                return answer.text, link, ans_selector

        # return "Couldn't ", ""

    def process_answer(self, answer: str) -> str:
        if not answer.endswith("..."):
            return answer

        sentences = answer.split(". ")
        if len(sentences[-1]) < 8:
            sentences = sentences[:-1]  # omit last sentence

        return ". ".join(sentences)

    @commands.command("ggl")
    async def gwogle_search(self, ctx: commands.Context, *query):
        """The main function of the package that puts everything together"""

        data = await get_url(
            f"https://google.com/search?q={'+'.join(query)}", text=True
        )
        print(data, file=open("text.html", "w"))
        raw_answer, link, _ = self.scrape_data(data)
        answer = self.process_answer(raw_answer)
        await ctx.send(embed=google_embed(" ".join(query), f"{answer}\n{link}"))

    @commands.command("google")
    async def main(self, ctx: commands.Context, *query):
        """The main function of the package that puts everything together"""

        data = await get_url(
            f"https://google.com/search?q={'+'.join(query)}", text=True
        )
        print(data, file=open("text.html", "w"))
        raw_answer, link, selector = self.scrape_data(data)
        answer = self.process_answer(raw_answer)
        await ctx.send(
            embed=google_embed(" ".join(query), f"{answer}\n{link}\n`{selector}`")
        )


def setup(bot):
    bot.add_cog(Google(bot))
