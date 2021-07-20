import asyncio

import aiohttp
import pymongo
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from moddy.utils import console, remove_prefix  # noqa: F401

from .database import database as db

loop = asyncio.get_event_loop()

quiz_coll = db.quiz
languages = ["python", "javascript"]


async def get_quiz(language: str) -> BeautifulSoup:
    url = f"https://www.tutorialspoint.com/{language}/{language}_online_quiz.htm"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
    return BeautifulSoup(html, "lxml")


async def quiz_html2json(lang, quiz):
    question: Tag = quiz.select_one(".Q")
    id: str = question.get("id")
    found = await quiz_coll.find_one({"id": id, "language": lang})
    ptags: ResultSet[Tag] = question.find_all(recursive=False)

    if found or 4 < len(ptags) > 6 or ptags[1].name not in ("pre", "p", "div"):
        console.log(id)
        return

    answers = question.select("p a")
    answer_dict = {}
    for answer in answers:
        letter, answer_text = answer.text.split(" - ")
        answer_dict[letter] = answer_text

    if len(ptags) == 6:
        code = ptags[1].text

    else:
        code = None

    title = remove_prefix(ptags[0].find(text=True, recursive=False), " - ")
    correct_answer = question.select_one("p .true span").text
    expla = quiz.select_one(".A p")

    schema = {
        "id": id,
        "language": lang,
        "title": title,
        "code": code,
        "answers": answer_dict,
        "correct_answer": correct_answer,
        "explanation": expla and expla.text,
    }

    asyncio.create_task(insert_doc(schema))


async def scrape(lang: str):
    soup = await get_quiz(lang)
    quizes = soup.select(".QA")  # select div with QA class
    for quiz in quizes:
        asyncio.create_task(quiz_html2json(lang, quiz))


async def insert_doc(doc: dict):
    try:
        await quiz_coll.insert_one(doc)

    except pymongo.errors.DuplicationError:
        pass


async def main():
    for language in languages:
        for _ in range(120):
            await scrape(language)


if __name__ == "__main__":
    try:
        loop.run_until_complete(main())

    finally:
        loop.close()
