from typing import Optional

from pydantic import BaseModel


class QuizModel(BaseModel):
    title: str
    answers: dict
    correct_answer: str
    explanation: str
