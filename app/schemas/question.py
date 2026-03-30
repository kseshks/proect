from typing import List

from pydantic import BaseModel, Field

from app.schemas import AnswerCreate, AnswerResponse


class QuestionBase(BaseModel):
    question_text: str = Field(..., min_length=1)
    question_type: str = Field(default="single_choice")
    points: float = Field(default=1.0, ge=0)

class QuestionCreate(QuestionBase):
    test_id: int
    answers: List["AnswerCreate"] = []

class QuestionUpdate(BaseModel):
    question_text: str | None = None
    question_type: str | None = None
    points: float | None = None

class QuestionResponse(QuestionBase):
    id: int
    test_id: int
    answers: List["AnswerResponse"] = []

    class Config:
        from_attributes = True