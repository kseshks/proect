from pydantic import BaseModel, Field


class SectionCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class SectionResponse(BaseModel):
    id: int
    title: str
    description: str | None
    teacher_id: int

    class Config:
        from_attributes = True