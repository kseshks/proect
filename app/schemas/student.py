from pydantic import BaseModel


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
