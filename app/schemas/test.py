from typing import List

from pydantic import BaseModel, Field


class TestBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

class TestCreate(TestBase):
    pass

class TestUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)

class TestResponse(TestBase):
    id: int
    teacher_id: int

    class Config:
        from_attributes = True

class TestDetailResponse(TestResponse):
    questions: List["QuestionResponse"] = []
    class Config:
        from_attributes = True