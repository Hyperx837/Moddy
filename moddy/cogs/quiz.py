# -*- coding: utf-8 -*-
import asyncio

import discord
import moddy.bot
from discord.ext import commands
from moddy.embeds import ModdyEmbed
from moddy.utils import get_mention, log, numbers, reloadr
from motor.motor_asyncio import AsyncIOMotorCollection


reloadr()


class Quiz(commands.Cog):
    """The description for Quiz goes here."""

    def __init__(self, bot):
        self.bot: moddy.bot.DiscordBot = bot

    async def get_question(self):
        quiz_coll: AsyncIOMotorCollection = self.bot.db.quiz  # gets quiz collection
        (self.question,) = [
            doc async for doc in quiz_coll.aggregate([{"$sample": {"size": 1}}])
        ]  # get random question from db

    @commands.command(name="quiz")
    async def quiz(self, ctx: commands.Context):
        log(get_mention(ctx.author), f"Requested a quiz with {ctx.message.content}")
        await self.get_question()
        title, answers = self.parse_data()
        msg: discord.Message = await ctx.send(
            embed=ModdyEmbed(title=title, description=answers)
        )
        await asyncio.gather(*(msg.add_reaction(num) for num in numbers.values()))

    def parse_data(self):
        ques = self.question
        answers = "\n".join(
            f"{i}. {ans}" for i, ans in enumerate(ques["answers"].values(), 1)
        )
        code: str = ques["code"]
        if code:
            if code.count("\n") > 1:
                answers = f"```py\n{code}```\n{answers}"
            else:
                answers = f"`{code}`\n{answers}"
        return ques["title"], answers

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        msg: discord.Message = reaction.message
        emoji: discord.Emoji = reaction.emoji
        # if bot was the one to react to the message or reaction was added to another message
        if user == self.bot.user or self.bot.user != msg.author:
            return

        log(
            f'question "{msg.content[:20]}..." was reacted {emoji} by user "{get_mention(user)}'
        )
        log(f"Guild: {msg.guild} | Channel: {msg.channel}")
        correct_answer = self.question["correct_answer"]
        correct_reaction = numbers[correct_answer]
        result = (
            "I knew that you were the only one who was going to get it the first time"
            if emoji == correct_reaction
            else "I had told my friend that you might cause a nexus event if you get it right the first time"
        )

        await user.send(result)
        await msg.remove_reaction(reaction.emoji, user)


def setup(bot):
    bot.add_cog(Quiz(bot))
