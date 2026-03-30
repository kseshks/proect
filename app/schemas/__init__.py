from .auth import LoginRequest, Token, TokenData
from .teacher import TeacherBase, TeacherCreate, TeacherUpdate, TeacherResponse
from .student import (
    StudentBase, StudentCreate,
    StudentResponse, StudentRegistrationResponse, StudentResultsResponse
)
from .test import TestBase, TestCreate, TestUpdate, TestResponse, TestDetailResponse
from .question import QuestionBase, QuestionCreate, QuestionUpdate, QuestionResponse
from .answer import AnswerBase, AnswerCreate, AnswerUpdate, AnswerResponse
from .test_result import (
    TestResultBase, TestResultCreate, TestResultUpdate,
    TestResultResponse, TestResultDetailResponse
)
from .student_answer import (
    StudentAnswerBase, StudentAnswerCreate, StudentAnswerResponse, SubmitAnswerRequest
)

__all__ = [
    # Auth
    "LoginRequest", "Token", "TokenData",
    # Teacher
    "TeacherBase", "TeacherCreate", "TeacherUpdate", "TeacherResponse",
    # Student
    "StudentBase", "StudentCreate", "StudentResponse",
    "StudentRegistrationResponse", "StudentResultsResponse",
    # Test
    "TestBase", "TestCreate", "TestUpdate", "TestResponse", "TestDetailResponse",
    # Question
    "QuestionBase", "QuestionCreate", "QuestionUpdate", "QuestionResponse",
    # Answer
    "AnswerBase", "AnswerCreate", "AnswerUpdate", "AnswerResponse",
    # TestResult
    "TestResultBase", "TestResultCreate", "TestResultUpdate",
    "TestResultResponse", "TestResultDetailResponse",
    # StudentAnswer
    "StudentAnswerBase", "StudentAnswerCreate", "StudentAnswerResponse", "SubmitAnswerRequest",
]