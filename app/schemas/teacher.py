from pydantic import BaseModel, EmailStr, Field


class TeacherBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class TeacherCreate(TeacherBase):
    password: str = Field(..., min_length=8)

class TeacherUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = Field(None, min_length=8)

class TeacherResponse(TeacherBase):
    id: int

    class Config:
        from_attributes = True
