from typing import List

from pydantic import BaseModel, Field

from app.schemas import QuestionResponse, QuestionCreate


class TestBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

class TestWithQuestionsCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    questions: List[QuestionCreate] = []

class TestWithQuestionsResponse(BaseModel):
    id: int
    title: str
    questions_count: int
    total_points: float
    message: str = "Тест успешно создан"

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