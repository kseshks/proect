from pydantic import BaseModel, Field


class TeacherBatchGenerateRequest(BaseModel):
    count: int = Field(1, ge=1, le=100)


class TeacherResponse(BaseModel):
    id: int
    login: str

    class Config:
        from_attributes = True


class TeacherCredentialResponse(BaseModel):
    id: int
    login: str
    password: str