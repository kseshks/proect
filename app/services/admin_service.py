from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import Teacher, ClassRoom, Student
from app.services.student_generation_service import generate_teacher_login, generate_password, generate_student_number


def create_teachers_batch(db: Session, count: int) -> list[dict]:
    created = []

    for _ in range(count):
        login = generate_teacher_login()
        while db.query(Teacher).filter(Teacher.login == login).first():
            login = generate_teacher_login()

        password = generate_password()
        teacher = Teacher(login=login, hashed_password=get_password_hash(password))
        db.add(teacher)
        db.flush()

        created.append({
            "id": teacher.id,
            "login": login,
            "password": password
        })

    db.commit()
    return created

def get_or_create_classroom(db: Session, class_name: str) -> ClassRoom:
    classroom: ClassRoom | None = db.query(ClassRoom).filter(ClassRoom.name == class_name).first()
    if classroom:
        return classroom

    classroom = ClassRoom(name=class_name)
    db.add(classroom)
    db.flush()
    return classroom

def create_classroom(db: Session, name: str, teacher_id: int | None = None) -> ClassRoom:
    existing = db.query(ClassRoom).filter(ClassRoom.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Такой класс уже существует")

    classroom = ClassRoom(name=name, teacher_id=teacher_id)
    db.add(classroom)
    db.commit()
    db.refresh(classroom)
    return classroom

def generate_students_for_class(db: Session, class_name: str, count: int) -> dict:
    classroom = get_or_create_classroom(db, class_name)
    created = []

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

        created.append({
            "id": student.id,
            "student_number": student_number,
            "password": password,
            "class_id": classroom.id,
            "class_name": classroom.name
        })

    db.commit()

    return {
        "class_id": classroom.id,
        "class_name": classroom.name,
        "students": created
    }