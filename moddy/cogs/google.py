# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Tuple, Type

from bs4 import BeautifulSoup, Tag
from discord.ext import commands
from moddy.embeds import google_embed
from moddy.utils import get_mention, get_url, log, reloadr

reloadr()


class Google(commands.Cog):
    """The description for Google goes here."""

    def __init__(self, bot):
        self.bot = bot

    @lru_cache(maxsize=50)
    def scrape_data(self, data) -> Tuple[str, str, str, str]:
        soup = BeautifulSoup(data, "lxml")
        answer_selectors = {
            "div.wDYxhc:nth-child(2) > div.IZ6rdc": "",  # main paragraph
            ".Z0LcW": "",  # highlted result
            ".XDTKBd": "",  # main result
            ".hgKElc": ".yuRUbf > a",  # featured snippet
            ".kno-rdesc > span:nth-child(2)": "",  # sidebar result
            ".VwiC3b": ".yuRUbf > a",  # first result
        }

        img_selectors = {"g-img.ivg-i": "data-lpage", "#dimg_46": "src"}

        for ans_selector, link_selector in answer_selectors.items():
            answer: Tag = soup.select_one(ans_selector)
            if answer and answer.text:
                link: str = (
                    f'[Read More....]({soup.select_one(link_selector)["href"]})'
                    if link_selector
                    else ""
                )
                break

        for img_selector, source_attr in img_selectors.items():
            img: Tag = soup.select_one(img_selector)
            if img:
                img_src = img.get(source_attr)
                break

        return answer.text, link, ans_selector, img_src

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
        raw_answer, link, selector, img = self.scrape_data(data)
        log(
            get_mention(ctx.author),
            f'got an answer for question "{" ".join(query)}" with {selector}',
        )
        answer = self.process_answer(raw_answer)
        await ctx.send(
            embed=google_embed(" ".join(query), f"{answer}\n{link}", img=img)
        )

    @commands.command("google")
    async def search(self, ctx: commands.Context, *query):
        """The main function of the package that puts everything together"""

        data = await get_url(
            f"https://google.com/search?q={'+'.join(query)}", text=True
        )
        print(data, file=open("text.html", "w"))
        raw_answer, link, selector, _ = self.scrape_data(data)
        answer = self.process_answer(raw_answer)
        await ctx.send(
            embed=google_embed(" ".join(query), f"{answer}\n{link}\n`{selector}`")
        )

    @search.error
    async def foo(ctx: commands.Context, error: Type[commands.CommandError]):  # type: ignore[return]
        log(get_mention(ctx.author), f"Caused the error {error}")


def setup(bot):
    bot.add_cog(Google(bot))
