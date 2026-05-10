from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_student
from app.core.database import get_db
from app.schemas.topic import AskQuestionRequest
from app.services.student_service import (ask_question, get_student_dialog, get_student_topic_detail, get_student_topics, get_student_sections, get_section_topics_for_student)

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


@router.get("/sections")
def student_sections(db: Session = Depends(get_db), student=Depends(require_student)):
    """Получение разделов, назначенных ученику целиком"""
    return get_student_sections(db, student.id)


@router.get("/sections/{section_id}/topics")
def student_section_topics(
    section_id: int, 
    db: Session = Depends(get_db), 
    student=Depends(require_student)
):
    """Получение всех тем раздела (если раздел назначен ученику)"""
    return get_section_topics_for_student(db, student.id, section_id)