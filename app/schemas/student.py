from pydantic import BaseModel, Field


class StudentsBatchCreateRequest(BaseModel):
    class_name: str = Field(..., min_length=1, max_length=50)
    count: int = Field(..., ge=1, le=200)

class TeacherStudentsGenerateRequest(BaseModel):
    count: int = Field(..., ge=1, le=200)


class StudentResponse(BaseModel):
    id: int
    student_number: str
    class_id: int

    class Config:
        from_attributes = True


class StudentCredentialResponse(BaseModel):
    id: int
    student_number: str
    password: str
    class_id: int
    class_name: str