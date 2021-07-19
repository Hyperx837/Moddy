from typing import Dict, Iterator, List

import discord
from typing_extensions import Literal

from .database.database import QuizModel, database


class Question(QuizModel):
    answered_users: list = []
    language: Literal["python", "javascript"]

    def has_answered(self, user):
        return user in self.answered_users

    def answered_by(self, author: discord.Member):
        self.answered_users.append(author)
        print(author)


class DictStack:
    def __init__(self) -> None:
        self._dict: Dict[int, Question] = {}
        self.coll = database["message_mapper"]

    async def setitem(self, key, item) -> None:
        if not isinstance(key, int):
            raise ValueError(
                f"Key of {self.__class__.__name__} cannot be type {type(key).__name__}"
            )

        self._dict[key] = Question(**item)
        item["msg_id"] = key
        await self.coll.insert_one(item)
        if len(self._dict) > 10:
            self._dict.popitem()

    async def getitem(self, key) -> Question:
        if key in self._dict:
            return self._dict[key]

        msg = await self.coll.find_one({"msg_id": key})
        if not msg:
            raise KeyError(f"Key {key} not found in either db or cache")
        return Question(**msg)

    async def random_questions(self, filt: dict, amount: int) -> List[Question]:
        pipeline = [{"$match": filt}, {"$sample": {"size": amount}}]
        # return [Question(**doc) async for doc in database.quiz.aggregate(pipeline)]
        lst = []
        async for doc in database.quiz.aggregate(pipeline):
            lst.append(Question(**doc))
            print(doc)
        return lst

        # yield Question(**doc)

    def __iter__(self) -> Iterator:
        return iter(self._dict)
