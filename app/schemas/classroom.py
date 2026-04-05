from pydantic import BaseModel, Field


class ClassCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    teacher_id: int | None = None


class ClassResponse(BaseModel):
    id: int
    name: str
    teacher_id: int | None = None

    class Config:
        from_attributes = True