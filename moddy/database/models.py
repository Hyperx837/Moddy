from typing import Optional

from pydantic import BaseModel


class QuizModel(BaseModel):
    id: str
    title: str
    code: Optional[str]
    answers: dict
    correct_answer: str
    explanation: str
