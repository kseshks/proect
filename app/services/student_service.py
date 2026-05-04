from typing import cast

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import SectionAssignment
from app.models.topic import Topic
from app.models.topic_assignment import TopicAssignment
from app.models.topic_dialog_message import TopicDialogMessage
from app.models.topic_question import TopicQuestion
from app.models.student import Student
from app.services.ai_service import build_topic_context, ask_deepseek


def get_student_topics(db: Session, student_id: int) -> list[dict]:
    topics_by_id = {}

    # 1. Темы, назначенные напрямую
    topic_assignments = db.query(TopicAssignment).filter(
        TopicAssignment.student_id == student_id
    ).all()

    for assignment in topic_assignments:
        topic = assignment.topic
        topics_by_id[topic.id] = topic

    # 2. Темы из назначенных разделов
    section_assignments = db.query(SectionAssignment).filter(
        SectionAssignment.student_id == student_id
    ).all()

    for assignment in section_assignments:
        section = assignment.section

        for topic in section.topics:
            topics_by_id[topic.id] = topic

    result = []

    for topic in topics_by_id.values():
        result.append({
            "id": topic.id,
            "title": topic.title,
            "description": topic.description,
            "section_id": topic.section_id
        })

    return result


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

    answer = ask_deepseek(
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