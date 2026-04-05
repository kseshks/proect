from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_student
from app.core.database import get_db
from app.schemas.topic import AskQuestionRequest
from app.services.student_service import (ask_question, get_student_dialog, get_student_topic_detail, get_student_topics)

router = APIRouter(prefix="/student", tags=["student"])


@router.get("/topics")
def student_topics(db: Session = Depends(get_db), student=Depends(require_student)):
    return get_student_topics(db, student.id)


@router.get("/topics/{topic_id}")
def student_topic_detail(topic_id: int, db: Session = Depends(get_db), student=Depends(require_student)):
    return get_student_topic_detail(db, student, topic_id)


@router.get("/topics/{topic_id}/dialog")
def student_dialog(topic_id: int, db: Session = Depends(get_db), student=Depends(require_student)):
    return get_student_dialog(db, student, topic_id)


@router.post("/topics/{topic_id}/ask")
def student_ask(
    topic_id: int,
    data: AskQuestionRequest,
    db: Session = Depends(get_db),
    student=Depends(require_student)
):
    return ask_question(db, student, topic_id, data.question_id)