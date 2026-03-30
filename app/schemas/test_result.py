from typing import List

from pydantic import BaseModel

from app.schemas import StudentAnswerResponse


class TestResultBase(BaseModel):
    total_points: float = 0.0
    max_points: float = 0.0

class TestResultCreate(TestResultBase):
    student_id: int
    test_id: int

class TestResultUpdate(TestResultBase):
    total_points: float | None = None
    max_points: float | None = None

class TestResultResponse(TestResultBase):
    id: int
    student_id: int
    test_id: int
    test_title: str | None = None
    result: str | None = None

    class Config:
        from_attributes = True

class TestResultDetailResponse(TestResultResponse):
    student_answers: List["StudentAnswerResponse"] = []

    class Config:
        from_attributes = True

