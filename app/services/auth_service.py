from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.teacher import Teacher
from app.models.student import Student
from app.core.security import verify_password, create_access_token
from app.schemas.auth import Token


def authenticate_teacher(db: Session, username: str, password: str):
    teacher = db.query(Teacher).filter(Teacher.email == username).first()
    if not teacher:
        return None
    if not verify_password(password, teacher.hashed_password):
        return None
    return teacher

def authenticate_student(db: Session, username: str, password: str):
    student = db.query(Student).filter(Student.login == username).first()
    if not student:
        return None
    if not verify_password(password, student.hashed_password):
        return None
    return student

def log_in(db: Session, username: str, password: str) -> Token:
    teacher = authenticate_teacher(db, username, password)
    if teacher:
        access_token = create_access_token(
            data={
                "sub": teacher.email,
                "user_id": teacher.id,
                "user_type": "teacher"
            }
        )
        return Token(access_token=access_token, token_type="bearer", user_type="teacher")

    student = authenticate_student(db, username, password)
    if student:
        access_token = create_access_token(
            data={
                "sub": student.login,
                "user_id": student.id,
                "user_type": "student"
            }
        )
        return Token(access_token=access_token, token_type="bearer", user_type="student")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный логин или пароль",
        headers={"WWW-Authenticate": "Bearer"},
    )