# -*- coding: utf-8 -*-

import asyncio
import random

import discord
import moddy.bot
from discord.ext import commands
from moddy import datastructures
from moddy.database.get_data import scrape
from moddy.datastructures import DictStack, Question
from moddy.embeds import ModdyEmbed, ModdySuccess
from moddy.utils import benchmark, get_mention, languages, log, numbers, reloadr

reloadr(datastructures)


class Quiz(commands.Cog):
    """The description for Quiz goes here."""

    def __init__(self, bot):
        self.bot: moddy.bot.DiscordBot = bot
        self.questions: DictStack = DictStack()

    def parse_data(self, ques: Question):
        answers = "\n".join(
            f"{i}. {ans}" for i, ans in enumerate(ques.answers.values(), 1)
        )
        code: str = ques.code
        if code:
            if code.count("\n") > 1:
                answers = f"```py\n{code}```\n{answers}"
            else:
                answers = f"`{code}`\n{answers}"
        question = f"{ques.title} ({ques.language})"  # question with language
        return question, answers

    @commands.command(name="quiz")
    async def quiz(self, ctx: commands.Context, lang: str = ""):
        log(get_mention(ctx.author), f"Requested a quiz with {ctx.message.content}")
        lang = lang or random.choice(languages)
        (question,) = await self.questions.random_questions({"language": lang}, 1)
        title, answers = self.parse_data(question)
        msg: discord.Message = await ctx.send(
            embed=ModdyEmbed(title=title, description=answers)
        )
        print(msg.id)
        await self.questions.setitem(msg.id, question.dict())
        await asyncio.gather(*(msg.add_reaction(num) for num in numbers.values()))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        member: discord.Member = await channel.guild.fetch_member(payload.user_id)
        msg: discord.Message = await channel.fetch_message(payload.message_id)
        emoji: str = payload.emoji._as_reaction()
        self.question: Question = await self.questions.getitem(msg.id)
        # if bot was the one to react to the message or reaction was added to another message
        conds = (
            member == self.bot.user,
            self.bot.user != msg.author,
        )
        if any(conds):
            return

        asyncio.create_task(msg.remove_reaction(emoji, member))
        if self.question.has_answered(member):
            return
        log(
            f'question "{msg.embeds[0].title[:20]}..." was reacted {emoji} by user {get_mention(member)}'
        )
        log(f"Guild: {msg.guild} | Channel: {msg.channel}")
        self.question.answered_by(member)
        correct_answer = self.question.correct_answer
        correct_reaction = numbers[correct_answer]
        result = (
            "I knew that you were the only one who was going to get it the first time"
            if emoji == correct_reaction
            else "I had told my friend that you might cause a nexus event if you get it right the first time"
        )

        await member.send(result)

    @commands.command("new-quizes")
    @commands.is_owner()
    async def download_quizes(self, ctx: commands.Context, lang: str, limit: int):
        await ctx.send(embed=ModdyEmbed("Starting Operation ✨ ... "))
        with benchmark() as timer:
            for _ in range(limit):
                await scrape(lang)

        title = "Operation Successful 🚀 ..."
        desc = f'Successfully pushed {limit} quizes about "{lang}" in {timer.elapsed}s.'
        await ctx.send(embed=ModdySuccess(title, desc))


def setup(bot):
    bot.add_cog(Quiz(bot))
