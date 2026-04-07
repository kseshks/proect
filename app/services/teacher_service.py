from os import PathLike
from pathlib import Path
from typing import cast
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import (
    ClassRoom,
    Student,
    Topic,
    TopicAssignment,
    TopicMaterial,
    TopicQuestion,
)
from app.services.material_processing_service import extract_text_from_url, extract_text_from_file, validate_file, \
    MAX_FILE_SIZE_MB
from app.services.student_generation_service import generate_student_number, generate_password

UPLOAD_DIR = Path("static/uploads/topics")

def get_teacher_classes(db: Session, teacher_id: int) -> list[ClassRoom]:
    classes: list[ClassRoom] = cast(
        list[ClassRoom],
        db.query(ClassRoom)
        .filter(ClassRoom.teacher_id == teacher_id)
        .order_by(ClassRoom.id.desc())
        .all()
    )
    return classes


def get_teacher_class_or_404(db: Session, teacher_id: int, class_id: int) -> ClassRoom:
    classroom = db.query(ClassRoom).filter(
        ClassRoom.id == class_id,
        ClassRoom.teacher_id == teacher_id
    ).first()

    if not classroom:
        raise HTTPException(status_code=404, detail="Класс не найден")

    return cast(ClassRoom, classroom)


def create_classroom_for_teacher(db: Session, teacher_id: int, name: str) -> ClassRoom:
    existing = db.query(ClassRoom).filter(ClassRoom.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Класс с таким названием уже существует")

    classroom = ClassRoom(
        name=name,
        teacher_id=teacher_id
    )
    db.add(classroom)
    db.commit()
    db.refresh(classroom)
    return classroom


def delete_classroom_for_teacher(db: Session, teacher_id: int, class_id: int) -> None:
    classroom = get_teacher_class_or_404(db, teacher_id, class_id)
    db.delete(classroom)
    db.commit()

def get_teacher_class_students(db: Session, teacher_id: int, class_id: int) -> list[Student]:
    _ = get_teacher_class_or_404(db, teacher_id, class_id)

    students: list[Student] = cast(
        list[Student],
        db.query(Student)
        .filter(Student.class_id == class_id)
        .order_by(Student.id.asc())
        .all()
    )
    return students


def generate_students_for_teacher_class(
    db: Session,
    teacher_id: int,
    class_id: int,
    count: int
) -> dict:
    classroom = get_teacher_class_or_404(db, teacher_id, class_id)

    created_students = []

    for _ in range(count):
        student_number = generate_student_number()
        password = generate_password()

        while db.query(Student).filter(Student.student_number == student_number).first():
            student_number = generate_student_number()

        student = Student(
            student_number=student_number,
            hashed_password=get_password_hash(password),
            class_id=classroom.id
        )
        db.add(student)
        db.flush()

        created_students.append({
            "id": student.id,
            "student_number": student_number,
            "password": password
        })

    db.commit()

    return {
        "class_id": classroom.id,
        "class_name": classroom.name,
        "students": created_students
    }


def delete_student_for_teacher(db: Session, teacher_id: int, student_id: int) -> None:
    student = db.query(Student).join(ClassRoom, Student.class_id == ClassRoom.id).filter(
        Student.id == student_id,
        ClassRoom.teacher_id == teacher_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Ученик не найден")

    db.delete(student)
    db.commit()

def create_topic(db: Session, teacher_id: int, title: str, description: str | None) -> Topic:
    topic = Topic(
        title=title,
        description=description,
        teacher_id=teacher_id
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def get_teacher_topic_or_404(db: Session, teacher_id: int, topic_id: int) -> Topic:
    topic = db.query(Topic).filter(
        Topic.id == topic_id,
        Topic.teacher_id == teacher_id
    ).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Тема не найдена")

    return cast(Topic, topic)


def get_teacher_topics(db: Session, teacher_id: int) -> list[Topic]:
    topics: list[Topic] = cast(
        list[Topic],
        db.query(Topic)
        .filter(Topic.teacher_id == teacher_id)
        .order_by(Topic.id.desc())
        .all()
    )
    return topics


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

def get_teacher_topic_materials(db: Session, teacher_id: int, topic_id: int) -> list[TopicMaterial]:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)

    materials: list[TopicMaterial] = cast(
        list[TopicMaterial],
        db.query(TopicMaterial)
        .filter(TopicMaterial.topic_id == topic.id)
        .order_by(TopicMaterial.id.asc())
        .all()
    )
    return materials


def add_link_material(db: Session, teacher_id: int, topic_id: int, title: str | None, url: str) -> TopicMaterial:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)

    material = TopicMaterial(
        topic_id=topic.id,
        material_type="link",
        title=title,
        url=url,
        parse_status="pending"
    )
    db.add(material)
    db.flush()

    try:
        material.extracted_text = extract_text_from_url(url)
        material.parse_status = "success"
    except Exception:
        material.extracted_text = None
        material.parse_status = "failed"

    db.commit()
    db.refresh(material)
    return material


def add_file_material(db: Session, teacher_id: int, topic_id: int, file: UploadFile) -> TopicMaterial:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)

    validate_file(file.filename)

    content = file.file.read()

    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_size_bytes:
        raise HTTPException(status_code=400, detail="Файл слишком большой")

    topic_dir = UPLOAD_DIR / str(topic.id)
    topic_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}_{file.filename}"
    target_path = topic_dir / filename

    with target_path.open("wb") as f:
        f.write(content)

    material = TopicMaterial(
        topic_id=topic.id,
        material_type="file",
        title=file.filename,
        file_path=str(target_path).replace("\\", "/"),
        parse_status="pending"
    )
    db.add(material)
    db.flush()

    try:
        material.extracted_text = extract_text_from_file(str(target_path))
        material.parse_status = "success"
    except Exception:
        material.extracted_text = None
        material.parse_status = "failed"

    db.commit()
    db.refresh(material)
    return material


def delete_material(db: Session, teacher_id: int, material_id: int) -> None:
    material = db.query(TopicMaterial).join(Topic, TopicMaterial.topic_id == Topic.id).filter(
        TopicMaterial.id == material_id,
        Topic.teacher_id == teacher_id
    ).first()

    if not material:
        raise HTTPException(status_code=404, detail="Материал не найден")

    if material.material_type == "file" and material.file_path:
        file_path = Path(cast(str | PathLike[str], material.file_path))
        if file_path.exists():
            file_path.unlink(missing_ok=True)

    db.delete(material)
    db.commit()

def get_topic_questions(db: Session, teacher_id: int, topic_id: int) -> list[TopicQuestion]:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)

    questions: list[TopicQuestion] = cast(
        list[TopicQuestion],
        db.query(TopicQuestion)
        .filter(TopicQuestion.topic_id == topic.id)
        .order_by(TopicQuestion.id.asc())
        .all()
    )
    return questions


def add_topic_questions(db: Session, teacher_id: int, topic_id: int, questions: list[dict]) -> list[TopicQuestion]:
    topic = get_teacher_topic_or_404(db, teacher_id, topic_id)

    for item in questions:
        question = TopicQuestion(
            topic_id=topic.id,
            text=item["text"]
        )
        db.add(question)

    db.commit()
    return get_topic_questions(db, teacher_id, topic_id)


def delete_question(db: Session, teacher_id: int, question_id: int) -> None:
    question = db.query(TopicQuestion).join(Topic, TopicQuestion.topic_id == Topic.id).filter(
        TopicQuestion.id == question_id,
        Topic.teacher_id == teacher_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    db.delete(question)
    db.commit()

def get_topic_assignment_options(db: Session, teacher_id: int, topic_id: int) -> dict:
    _ = get_teacher_topic_or_404(db, teacher_id, topic_id)
    classes = get_teacher_classes(db, teacher_id)

    result = []
    for classroom in classes:
        students = db.query(Student).filter(Student.class_id == classroom.id).order_by(Student.id.asc()).all()

        result.append({
            "id": classroom.id,
            "name": classroom.name,
            "students": [
                {
                    "id": student.id,
                    "student_number": student.student_number
                }
                for student in students
            ]
        })

    return {"classes": result}


def assign_topic(db: Session, teacher, topic_id: int, class_ids: list[int], student_numbers: list[str]) -> dict:
    topic = get_teacher_topic_or_404(db, teacher.id, topic_id)

    if not topic.questions:
        raise HTTPException(status_code=400, detail="Нельзя назначить тему без вопросов")

    if not topic.materials:
        raise HTTPException(status_code=400, detail="Нельзя назначить тему без материалов")

    student_ids = set()

    if class_ids:
        classes = db.query(ClassRoom).filter(
            ClassRoom.id.in_(class_ids),
            ClassRoom.teacher_id == teacher.id
        ).all()

        for classroom in classes:
            for student in classroom.students:
                student_ids.add(student.id)

    if student_numbers:
        students = db.query(Student).join(ClassRoom, Student.class_id == ClassRoom.id).filter(
            Student.student_number.in_(student_numbers),
            ClassRoom.teacher_id == teacher.id
        ).all()

        for student in students:
            student_ids.add(student.id)

    if not student_ids:
        raise HTTPException(status_code=400, detail="Не выбраны ученики или классы")

    created = 0
    for student_id in student_ids:
        exists = db.query(TopicAssignment).filter(
            TopicAssignment.topic_id == topic.id,
            TopicAssignment.student_id == student_id
        ).first()

        if exists:
            continue

        assignment = TopicAssignment(
            topic_id=topic.id,
            student_id=student_id,
            assigned_by_teacher_id=teacher.id
        )
        db.add(assignment)
        created += 1

    db.commit()

    return {
        "assigned_count": created,
        "selected_students_count": len(student_ids)
    }