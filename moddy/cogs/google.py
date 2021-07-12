# -*- coding: utf-8 -*-

import asyncio
from typing import Optional, Tuple

from bs4 import BeautifulSoup, Tag
from discord.ext import commands
from moddy.embeds import google_embed
from moddy.utils import get_mention, get_url, log, reloadr

reloadr()


class Google(commands.Cog):
    """The description for Google goes here."""

    def __init__(self, bot):
        self.bot = bot
        self.answer_selectors = {
            "div.wDYxhc:nth-child(2) > div.IZ6rdc": "",  # main paragraph
            ".Z0LcW": "",  # highlted result
            ".XDTKBd": "",  # main result
            ".hgKElc": ".yuRUbf > a",  # featured snippet
            ".kno-rdesc > span:nth-child(2)": "",  # sidebar result
            ".VwiC3b": ".yuRUbf > a",  # first result
        }
        self.img_selectors = {"g-img.ivg-i": "data-lpage"}

    def process_answer(self, answer: str) -> str:
        if not answer.endswith("..."):
            return answer

        # omit last sentence if it doesn't have more than 8 letters
        # 8 characters doesn't make a meaningful sentence
        sentences = answer.split(". ")
        if len(sentences[-1]) < 8:
            sentences = sentences[:-1]

        return ". ".join(sentences)

    def get_image(self) -> Optional[str]:
        for img_selector, source_attr in self.img_selectors.items():
            img: Tag = self.soup.select_one(img_selector)
            if img:
                print(img)
                return img.get(source_attr)
        return None

    def get_answer(self) -> str:
        for ans_selector, link_selector in self.answer_selectors.items():
            answer: Tag = self.soup.select_one(ans_selector)
            if answer and answer.text:
                link: str = (
                    f'[Read More....]({self.soup.select_one(link_selector)["href"]})'
                    if link_selector
                    else ""
                )
                answer = self.process_answer(answer.text)
                answer = f"{answer}\n{link}"
                break

        else:
            answer = (
                "Are you god? you just redendered google powerless with"
                f" just {len(self.search_term)} characters"
            )

        return answer

    def scrape_data(self, data) -> Tuple[str, Optional[str]]:
        self.soup = BeautifulSoup(data, "lxml")
        img_src = self.get_image()
        answer = self.get_answer()
        return answer, img_src

    async def search_google(self, query):
        data = await get_url(f"https://google.com/search?q={query}", text=True)
        print(data, file=open("text.html", "w"))

        answer, img = self.scrape_data(data)

        await self.send_message(embed=google_embed(query, answer, img=img))

    @commands.command("ggl")
    async def handle_query(self, ctx: commands.Context, *keywords):
        """The main function of the package that puts everything together"""
        self.send_message = ctx.send
        search_term = " ".join(keywords)
        self.search_term = search_term
        queries = search_term.split(" | ")
        print("+".join("- | -"))
        await asyncio.gather(*[self.search_google(query) for query in queries])

        log(
            get_mention(ctx.author),
            f'reuqested results for "{search_term}" in #{ctx.channel}',
        )


def setup(bot):
    bot.add_cog(Google(bot))
