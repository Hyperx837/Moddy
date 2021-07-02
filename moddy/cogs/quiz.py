# -*- coding: utf-8 -*-
import asyncio

import aiohttp
import discord
from discord.ext import commands
from discord.message import Message
from moddy.config import quizapi_token
from moddy.utils import ModdyEmbed, log, numbers

params = {"apiKey": quizapi_token, "limit": 1}


def parse_data(data: list):
    quiz: dict = data[0]
    area = quiz["tags"][0]["name"]
    question: str = f"{quiz['question']} ({area})"
    answers = enumerate((ans for ans in quiz["answers"].values() if ans), 1)
    answers_formatted: str = "\n".join(f"{idx}. {ans}" for idx, ans in answers)
    correct_answer, *_ = (
        idx for idx, ans in enumerate(quiz["correct_answers"].values()) if ans == "true"
    )
    return question, answers_formatted, correct_answer


async def get_quiz():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://quizapi.io/api/v1/questions", params=params
        ) as response:
            return await response.json()


class Quiz(commands.Cog):
    """The description for Quiz goes here."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name="quiz")
    async def send_quiz(self, ctx: commands.Context):
        log(f'[{ctx.author.color}]@{ctx.author.name}[/{ctx.author.color}] Requested a quiz with {ctx.message.content}')
        json_data = await get_quiz()
        question, answers, correct_answer = parse_data(json_data)
        msg: discord.Message = await ctx.send(
            embed=ModdyEmbed(title=question, description=answers)
        )
        self.quiz_id = msg.id
        self.correct_answer = correct_answer
        answer_count = answers.count("\n") + 1
        asyncio.gather(*(msg.add_reaction(num) for num in numbers[:answer_count]))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.id == self.bot.user.id or self.quiz_id != reaction.message.id:
            return

        log(f'[{user.color}]@{user.name}[/{user.color}] reacted to question "{reaction.message.id}" with a {reaction.emoji}')
        log(reaction.emoji)
        log(f'Guild: {reaction.message.guild} | Channel: {reaction.message.channel}')
        given_answer = numbers.index(reaction.emoji)
        msg = (
            "I knew that you were the only one who was going to get it the first time"
            if given_answer == self.correct_answer
            else "I had told my friend that you might cause a nexus event if you get it right the first time"
        )
        await user.send(msg)
        await reaction.message.remove_reaction(reaction.emoji, user)


def setup(bot):
    bot.add_cog(Quiz(bot))
