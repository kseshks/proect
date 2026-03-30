from pydantic import BaseModel


class StudentAnswerBase(BaseModel):
    answer_text: str
    is_correct: bool = False
    points_earned: float = 0.0

class StudentAnswerCreate(BaseModel):
    test_result_id: int
    question_id: int
    answer_text: str

class StudentAnswerResponse(StudentAnswerBase):
    id: int
    test_result_id: int
    question_id: int
    question_text: str | None = None
    correct_answer_text: str | None = None

    class Config:
        from_attributes = True

class SubmitAnswerRequest(BaseModel):
    question_id: int
    answer_text: str