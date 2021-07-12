# -*- coding: utf-8 -*-
import asyncio

import discord
from discord.ext import commands
from moddy.config import quizapi_token
from moddy.embeds import ModdyEmbed
from moddy.utils import get_mention, get_url, log, numbers, reloadr

params = {"apiKey": quizapi_token, "limit": 1}

reloadr()


def parse_data(data: list):
    quiz: dict = data[0]
    area = quiz["tags"][0]["name"]
    question: str = f"{quiz['question']} ({area})"
    answers = enumerate((ans for ans in quiz["answers"].values() if ans), 1)
    answers_formatted: str = "\n".join(f"{idx}. {ans}" for idx, ans in answers)
    correct_answer, *_ = (
        idx for idx, ans in enumerate(quiz["correct_answers"].values()) if ans == "true"
    )
    # discord.Guild.
    return question, answers_formatted, correct_answer


class Quiz(commands.Cog):
    """The description for Quiz goes here."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name="quiz")
    async def send_quiz(self, ctx: commands.Context):
        log(get_mention(ctx.author), f"Requested a quiz with {ctx.message.content}")
        json_data = await get_url(
            "https://quizapi.io/api/v1/questions", params=params, json=True
        )
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
        msg: discord.Message = reaction.message
        emoji: discord.Emoji = reaction.emoji
        if user == self.bot.user or self.bot.user != msg.author:
            return

        log(
            f'question "{msg.content[:20]}..." was reacted {emoji} by user "{get_mention(user)}'
        )
        log(emoji)
        log(f"Guild: {msg.guild} | Channel: {msg.channel}")
        given_answer = numbers.index(emoji)
        result = (
            "I knew that you were the only one who was going to get it the first time"
            if given_answer == self.correct_answer
            else "I had told my friend that you might cause a nexus event if you get it right the first time"
        )
        await user.send(result)
        await msg.remove_reaction(reaction.emoji, user)


def setup(bot):
    bot.add_cog(Quiz(bot))
