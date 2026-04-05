from pathlib import Path
from typing import cast
from uuid import uuid4

from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile

from app.models import ClassRoom, Student, Topic, TopicMaterial, TopicQuestion, Teacher, TopicAssignment

UPLOAD_DIR = Path("static/uploads/topics")

def get_teacher_classes(db: Session, teacher_id: int) -> list[ClassRoom]:
    classes: list[ClassRoom] = cast(list[ClassRoom], db.query(ClassRoom).filter(ClassRoom.teacher_id == teacher_id).all())
    return classes

def get_teacher_class_students(db: Session, teacher_id: int, class_id: int) -> list[Student]:
    classroom = db.query(ClassRoom).filter(
        ClassRoom.id == class_id,
        ClassRoom.teacher_id == teacher_id
    ).first()

    if not classroom:
        raise HTTPException(status_code=404, detail="Класс не найден")

    students: list[Student] = cast(list[Student], db.query(Student).filter(Student.class_id == class_id).all())
    return students

def create_topic(db: Session, teacher_id: int, title: str, description: str | None) -> Topic:
    topic = Topic(title=title, description=description, teacher_id=teacher_id)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic

def get_teacher_topic_or_404(db: Session, teacher_id: int, topic_id: int) -> Topic:
    topic: Topic = cast(Topic, db.query(Topic).filter(Topic.id == topic_id, Topic.teacher_id == teacher_id).first())
    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    return topic

def update_topic(db: Session, teacher_id: int, topic_id: int, data: dict) -> Topic:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)

    for key, value in data.items():
        if value is not None:
            setattr(topic, key, value)

    db.commit()
    db.refresh(topic)
    return topic

def delete_topic(db: Session, teacher_id: int, topic_id: int) -> None:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)
    db.delete(topic)
    db.commit()

def add_link_material(db: Session, teacher_id: int, topic_id: int, title: str | None, url: str) -> TopicMaterial:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)

    material = TopicMaterial(
        topic_id=topic.id,
        material_type="link",
        title=title,
        url=url
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

def add_file_material(db: Session, teacher_id: int, topic_id: int, file: UploadFile) -> TopicMaterial:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)

    topic_dir = UPLOAD_DIR / str(topic.id)
    topic_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}_{file.filename}"
    target_path = topic_dir / filename

    with target_path.open("wb") as f:
        f.write(file.file.read())

    material = TopicMaterial(
        topic_id=topic.id,
        material_type="file",
        title=file.filename,
        file_path=str(target_path).replace("\\", "/")
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

def get_topic_questions(db: Session, teacher_id: int, topic_id: int) -> list[TopicQuestion]:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)
    questions: list[TopicQuestion] = cast(list[TopicQuestion], db.query(TopicQuestion).filter(TopicQuestion.topic_id == topic.id).order_by(TopicQuestion.id).all())
    return questions

def add_topic_questions(db: Session, teacher_id: int, topic_id: int, questions: list[dict]) -> list[TopicQuestion]:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)

    created = []
    for item in questions:
        question = TopicQuestion(topic_id=topic.id, text=item["text"],)
        db.add(question)
        created.append(question)

    db.commit()
    return get_topic_questions(db, teacher_id, topic_id)

def assign_topic_to_students(db: Session, teacher: Teacher, topic_id: int, student_numbers: list[str]) -> dict:
    topic = get_teacher_topic_or_404(db, teacher.id, topic_id)

    students = db.query(Student).join(ClassRoom, Student.class_id == ClassRoom.id).filter(Student.student_number.in_(student_numbers),ClassRoom.teacher_id == teacher.id).all()

    if not students:
        raise HTTPException(status_code=404, detail="Ученики не найдены")

    created = 0
    for student in students:
        exists = db.query(TopicAssignment).filter(TopicAssignment.topic_id == topic.id, TopicAssignment.student_id == student.id).first()
        if exists:
            continue

        assignment = TopicAssignment(topic_id=topic.id, student_id=cast(int, student.id), assigned_by_teacher_id=teacher.id)
        db.add(assignment)
        created += 1

    db.commit()
    return {"assigned_count": created}

def assign_topic_to_classes(db: Session, teacher: Teacher, topic_id: int, class_ids: list[int]) -> dict:
    topic = get_teacher_topic_or_404(db, teacher.id, topic_id)

    classes = db.query(ClassRoom).filter(
        ClassRoom.id.in_(class_ids),
        ClassRoom.teacher_id == teacher.id
    ).all()

    if not classes:
        raise HTTPException(status_code=404, detail="Классы не найдены")

    students = db.query(Student).filter(Student.class_id.in_([c.id for c in classes])).all()

    created = 0
    for student in students:
        exists = db.query(TopicAssignment).filter(TopicAssignment.topic_id == topic.id, TopicAssignment.student_id == student.id).first()
        if exists:
            continue

        assignment = TopicAssignment(topic_id=topic.id, student_id=cast(int, student.id), assigned_by_teacher_id=teacher.id)
        db.add(assignment)
        created += 1

    db.commit()
    return {"assigned_count": created}