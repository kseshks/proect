from pydantic import BaseModel, Field


class TopicCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class TopicUpdateRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


class TopicResponse(BaseModel):
    id: int
    title: str
    description: str | None
    teacher_id: int

    class Config:
        from_attributes = True


class MaterialLinkCreateRequest(BaseModel):
    title: str | None = None
    url: str


class MaterialResponse(BaseModel):
    id: int
    material_type: str
    title: str | None = None
    url: str | None = None
    file_path: str | None = None

    class Config:
        from_attributes = True


class QuestionCreateRequest(BaseModel):
    text: str = Field(..., min_length=1)


class QuestionsBatchCreateRequest(BaseModel):
    questions: list[QuestionCreateRequest]


class QuestionResponse(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True


from pydantic import BaseModel, Field


class AssignTopicRequest(BaseModel):
    class_ids: list[int] = Field(default_factory=list)
    student_numbers: list[str] = Field(default_factory=list)


class AskQuestionRequest(BaseModel):
    question_id: int


class DialogMessageResponse(BaseModel):
    id: int
    question_id: int
    question_text: str
    answer_text: str

    class Config:
        from_attributes = True