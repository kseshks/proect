from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate
from app.core.security import get_password_hash

def create_teacher(db: Session, teacher_data: TeacherCreate) -> Teacher:
    existing = db.query(Teacher).filter(Teacher.email == teacher_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )
    db_teacher = Teacher(
        email=teacher_data.email,
        hashed_password=get_password_hash(teacher_data.password),
        first_name=teacher_data.first_name,
        last_name=teacher_data.last_name
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)

    return db_teacher
