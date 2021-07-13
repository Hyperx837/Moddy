import asyncio
from typing import Optional

import aiohttp
import pymongo
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pydantic import BaseModel
from rich.console import Console

from utils import remove_prefix

loop = asyncio.get_event_loop()
client = AsyncIOMotorClient("localhost", 27017, io_loop=loop)
console = Console()

db: AsyncIOMotorDatabase = client["moddity"]


class Question(BaseModel):
    id: str
    title: str
    code: Optional[str]
    answers: dict
    correct_answer: str
    explanation: str


async def scrape():
    collection: AsyncIOMotorCollection = db["quiz"]
    await collection.create_index([("id", pymongo.ASCENDING)], unique=True)
    url = "https://www.tutorialspoint.com/python/python_online_quiz.htm"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
    soup = BeautifulSoup(html, "lxml")

    quizes = soup.select(".QA")
    for quiz in quizes:
        question: Tag = quiz.select_one(".Q")
        id = question.get("id")
        found = await collection.find_one({"id": id})
        if found:
            continue
        answers = question.select("p a")
        answer_dict = {}
        for answer in answers:
            letter, answer_text = answer.text.split(" - ")
            answer_dict[letter] = answer_text

        ptags: ResultSet[Tag] = question.find_all(recursive=False)
        if len(ptags) > 6:
            continue
        if len(ptags) == 6:
            if ptags[1].name not in ("pre", "p"):
                continue
            code = ptags[1].text
        else:
            code = None

        expla = quiz.select_one(".A p")
        quiz_data = {
            "id": id,
            "language": "python",
            "title": remove_prefix(ptags[0].find(text=True, recursive=False), " - "),
            "code": code,
            "answers": answer_dict,
            "correct_answer": question.select_one("p .true span").text,
            "explanation": expla and expla.text,
        }
        try:
            await collection.insert_one(quiz_data)
            console.print(quiz_data)

        except pymongo.errors.DuplicationError:
            pass


async def main():
    await scrape()
    for _ in range(20):
        await asyncio.gather(*[scrape() for _ in range(6)])


if __name__ == "__main__":
    try:
        loop.run_until_complete(main())

    finally:
        loop.close()
