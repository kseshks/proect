from typing import cast

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.topic import Topic
from app.models.topic_assignment import TopicAssignment
from app.models.topic_dialog_message import TopicDialogMessage
from app.models.topic_question import TopicQuestion
from app.models.student import Student
from app.services.ai_service import generate_answer


def get_student_topics(db: Session, student_id: int) -> list[dict]:
    assignments = db.query(TopicAssignment).filter(TopicAssignment.student_id == student_id).all()

    result = []
    for assignment in assignments:
        topic = assignment.topic
        questions_count = len([q for q in topic.questions if q.is_active])
        result.append({
            "id": topic.id,
            "title": topic.title,
            "description": topic.description,
            "questions_count": questions_count
        })
    return result


def get_student_topic_or_404(db: Session, student: Student, topic_id: int) -> Topic:
    assignment = db.query(TopicAssignment).filter(
        TopicAssignment.topic_id == topic_id,
        TopicAssignment.student_id == student.id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Тема не назначена этому ученику")

    topic: Topic = cast(Topic, db.query(Topic).filter(Topic.id == topic_id).first())
    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")

    return topic


def get_student_topic_detail(db: Session, student: Student, topic_id: int) -> dict:
    topic = get_student_topic_or_404(db, student, topic_id)

    return {
        "id": topic.id,
        "title": topic.title,
        "description": topic.description,
        "materials": topic.materials,
        "questions": sorted([q for q in topic.questions if q.is_active], key=lambda x: (x.sort_order, x.id))
    }


def get_student_dialog(db: Session, student: Student, topic_id: int) -> list[TopicDialogMessage]:
    get_student_topic_or_404(db, student, topic_id)

    return cast(list[TopicDialogMessage], db.query(TopicDialogMessage).filter(TopicDialogMessage.topic_id == topic_id,TopicDialogMessage.student_id == student.id).order_by(TopicDialogMessage.id.asc()).all())

def ask_question(db: Session, student: Student, topic_id: int, question_id: int) -> TopicDialogMessage:
    topic = get_student_topic_or_404(db, student, topic_id)

    question = db.query(TopicQuestion).filter(TopicQuestion.id == question_id, TopicQuestion.topic_id == topic.id,).first()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    answer = generate_answer(topic, topic.materials, cast(str, question.text))

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