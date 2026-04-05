from .auth import LoginRequest, Token
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
    AssignStudentsRequest,
    AssignClassesRequest,
    AssignedStudentResponse,
    StudentTopicListResponse,
    StudentTopicDetailResponse,
    AskQuestionRequest,
    DialogMessageResponse,
)