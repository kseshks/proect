from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.config import settings
from app.models import Admin
from app.models.teacher import Teacher
from app.models.student import Student
from app.core.security import verify_password, create_access_token
from app.schemas.auth import Token

def authenticate_admin(db: Session, username: str, password: str) -> Admin | None:
    admin = db.query(Admin).filter(Admin.login == username).first()
    if admin and verify_password(password, admin.hashed_password):
        return admin
    return None

def authenticate_teacher(db: Session, username: str, password: str):
    teacher = db.query(Teacher).filter(Teacher.login == username).first()
    if teacher and verify_password(password, teacher.hashed_password):
        return teacher
    return None

def authenticate_student(db: Session, username: str, password: str):
    student = db.query(Student).filter(Student.student_number == username).first()
    if student and verify_password(password, student.hashed_password):
        return student
    return None

def login(db: Session, username: str, password: str) -> Token:
    admin = authenticate_admin(db, username, password)
    if admin:
        token = create_access_token(
            data={
                "sub": admin.login,
                "username": admin.id,
                "user_type": settings.ROLE_ADMIN
            }
        )
        return Token(access_token=token, token_type="bearer", user_type=settings.ROLE_ADMIN)

    teacher = authenticate_teacher(db, username, password)
    if teacher:
        token = create_access_token(
            data={
                "sub": teacher.login,
                "user_id": teacher.id,
                "user_type": settings.ROLE_TEACHER
            }
        )
        return Token(access_token=token, token_type="bearer", user_type=settings.ROLE_TEACHER)

    student = authenticate_student(db, username, password)
    if student:
        token = create_access_token(
            data={
                "sub": student.student_number,
                "user_id": student.id,
                "user_type": settings.ROLE_STUDENT
            }
        )
        return Token(access_token=token, token_type="bearer", user_type=settings.ROLE_STUDENT)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный логин или пароль",
        headers={"WWW-Authenticate": "Bearer"},
    )