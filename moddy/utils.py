import aiohttp
import discord

from moddy.config import quizapi_token


class ModdyMessage(discord.Embed):
    def __init__(self, title, description, **kwargs):
        super().__init__(**kwargs)
        self.color = 0xFFFFFF
        self.title = title
        self.description = description


params = {"apiKey": quizapi_token, "limit": 1}
# numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight"]


def parse_data(data: list):
    quiz: dict = data[0]
    area = quiz["tags"][0]["name"]
    question: str = f"{quiz['question']} ({area})"
    answers = enumerate((ans for ans in quiz["answers"].values() if ans), 1)
    answers_formatted: str = "\n".join(f"{idx}. {ans}" for idx, ans in answers)
    # correct_answer, *_ = (
    #     idx for idx, ans in enumerate(quiz["correct_answers"]) if ans == "true"
    # )
    return question, answers_formatted


async def get_quiz():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://quizapi.io/api/v1/questions", params=params
        ) as response:
            return await response.json()
