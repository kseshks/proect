from typing import List

from pydantic import BaseModel, Field

class StudentsBatchCreate(BaseModel):
    count: int = Field(..., ge=1, le=100, description="Количество учеников для создания")

class StudentRatingResponse(BaseModel):
    student_number: int
    total_points: float
    max_points: float
    result: str
    percentage: float

class TestRatingResponse(BaseModel):
    test_id: int
    test_title: str
    results: List[StudentRatingResponse]

class StudentBase(BaseModel):
    login: str
    student_number: int

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True

class StudentRegistrationResponse(BaseModel):
    login: str
    student_number: int
    password: str
    message: str

class StudentResultsResponse(BaseModel):
    test_id: int
    test_title: str
    total_points: float
    max_points: float
    result: str
