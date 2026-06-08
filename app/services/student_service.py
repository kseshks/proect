from typing import cast

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import SectionAssignment
from app.models.topic import Topic
from app.models.topic_assignment import TopicAssignment
from app.models.topic_dialog_message import TopicDialogMessage
from app.models.topic_question import TopicQuestion
from app.models.student import Student
from app.services.ai_service import build_topic_context, ask_nemotron


def get_student_topics(db: Session, student_id: int) -> list[dict]:
    topics_by_id = {}

    # 1. Темы, назначенные напрямую
    topic_assignments = db.query(TopicAssignment).filter(
        TopicAssignment.student_id == student_id
    ).all()

    for assignment in topic_assignments:
        topic = assignment.topic
        topics_by_id[topic.id] = {
            "id": topic.id,
            "title": topic.title,
            "section_id": topic.section_id,
            "section_title": topic.section.title if topic.section else "Без раздела"
        }

    # 2. Темы из назначенных разделов
    section_assignments = db.query(SectionAssignment).filter(
        SectionAssignment.student_id == student_id
    ).all()

    for assignment in section_assignments:
        section = assignment.section
        for topic in section.topics:
            if topic.id not in topics_by_id:
                topics_by_id[topic.id] = {
                    "id": topic.id,
                    "title": topic.title,
                    "section_id": topic.section_id,
                    "section_title": section.title
                }

    return list(topics_by_id.values())

def get_student_sections(db: Session, student_id: int) -> list[dict]:
    """Возвращает разделы, назначенные ученику целиком"""
    assignments = db.query(SectionAssignment).filter(
        SectionAssignment.student_id == student_id
    ).all()
    
    return [
        {
            "id": a.section.id,
            "title": a.section.title,
            "name": a.section.title
        }
        for a in assignments
    ]


def get_section_topics_for_student(db: Session, student_id: int, section_id: int) -> list[dict]:
    """Возвращает все темы раздела (если раздел назначен ученику)"""
    # Проверяем доступ
    assignment = db.query(SectionAssignment).filter(
        SectionAssignment.student_id == student_id,
        SectionAssignment.section_id == section_id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=403, detail="Раздел не назначен")
    
    topics = db.query(Topic).filter(
        Topic.section_id == section_id
    ).order_by(Topic.title).all()
    
    return [
        {
            "id": t.id,
            "title": t.title,
            "section_id": t.section_id,
            "section_title": assignment.section.title
        }
        for t in topics
    ]


def get_student_topic_or_404(db: Session, student: Student, topic_id: int) -> Topic:
    # 1. Проверяем прямое назначение темы
    direct_assignment = db.query(TopicAssignment).filter(
        TopicAssignment.topic_id == topic_id,
        TopicAssignment.student_id == student.id
    ).first()

    if direct_assignment:
        topic: Topic = cast(Topic, db.query(Topic).filter(Topic.id == topic_id).first())
        if not topic:
            raise HTTPException(status_code=404, detail="Тема не найдена")
        return topic

    # 2. Проверяем назначение через раздел
    section_assignment = db.query(SectionAssignment).join(
        Topic,
        Topic.section_id == SectionAssignment.section_id
    ).filter(
        Topic.id == topic_id,
        SectionAssignment.student_id == student.id
    ).first()

    if section_assignment:
        topic = cast(Topic, db.query(Topic).filter(Topic.id == topic_id).first())
        if not topic:
            raise HTTPException(status_code=404, detail="Тема не найдена")
        return topic

    raise HTTPException(status_code=404, detail="Тема не назначена этому ученику")


def get_student_topic_detail(db: Session, student: Student, topic_id: int) -> dict:
    topic = get_student_topic_or_404(db, student, topic_id)

    return {
        "id": topic.id,
        "title": topic.title,
        "description": topic.description,
        "materials": topic.materials,
        "questions": topic.questions  # ← Убрал сортировку по sort_order и is_active
    }


def get_student_dialog(db: Session, student: Student, topic_id: int) -> list[TopicDialogMessage]:
    get_student_topic_or_404(db, student, topic_id)

    return cast(list[TopicDialogMessage], 
        db.query(TopicDialogMessage)
        .filter(
            TopicDialogMessage.topic_id == topic_id,
            TopicDialogMessage.student_id == student.id
        )
        .order_by(TopicDialogMessage.id.asc())
        .all()
    )


def ask_question(db: Session, student: Student, topic_id: int, question_id: int) -> TopicDialogMessage:
    topic = get_student_topic_or_404(db, student, topic_id)

    question = db.query(TopicQuestion).filter(
        TopicQuestion.id == question_id,
        TopicQuestion.topic_id == topic.id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    context = build_topic_context(topic)

    answer = ask_nemotron(
    topic_title=topic.title,
    context=context,
    question_text=cast(str, question.text)
    )

    message = TopicDialogMessage(
        topic_id=topic.id,
        student_id=student.id,
        question_id=cast(int, question.id),
        question_text=cast(str, question.text),
        answer_text=answer
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return message