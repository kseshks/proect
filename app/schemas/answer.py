from pydantic import BaseModel, Field


class AnswerBase(BaseModel):
    answer_text: str = Field(..., min_length=1)
    is_correct: bool = False

class AnswerCreate(AnswerBase):
    question_id: int

class AnswerUpdate(BaseModel):
    answer_text: str | None = None
    is_correct: bool | None = None

class AnswerResponse(AnswerBase):
    id: int
    answer_id: int

    class Config:
        from_attributes = True