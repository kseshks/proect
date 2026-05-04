from .auth import LoginRequest, Token
from .section import SectionCreateRequest, SectionResponse
from .teacher import TeacherBatchGenerateRequest, TeacherResponse, TeacherCredentialResponse
from .classroom import ClassCreateRequest, ClassResponse
from .student import StudentsBatchCreateRequest, StudentResponse, StudentCredentialResponse
from .topic import (
    TopicCreateRequest,
    TopicUpdateRequest,
    TopicResponse,
    MaterialLinkCreateRequest,
    MaterialResponse,
    QuestionCreateRequest,
    QuestionsBatchCreateRequest,
    QuestionResponse,
    AssignTopicRequest,
    AskQuestionRequest,
    DialogMessageResponse,
)