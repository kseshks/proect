from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_token
from app.models import Admin
from app.models.teacher import Teacher
from app.models.student import Student

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен"
        )

    user_id = payload.get("user_id")
    user_type = payload.get("user_type")

    if user_type == settings.ROLE_ADMIN:
        user = db.query(Admin).filter(Admin.id == user_id).first()
    elif user_type == settings.ROLE_TEACHER:
        user = db.query(Teacher).filter(Teacher.id == user_id).first()
    elif user_type == settings.ROLE_STUDENT:
        user = db.query(Student).filter(Student.id == user_id).first()
    else:
        user = None

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )

    return user, user_type

def require_admin(current_user = Depends(get_current_user)):
    user, user_type = current_user
    if user_type != settings.ROLE_ADMIN:
        raise HTTPException(status_code=403, detail="Доступ только для администратора")
    return user

def require_teacher(current_user = Depends(get_current_user)):
    user, user_type = current_user
    if user_type != settings.ROLE_TEACHER:
        raise HTTPException(status_code=403, detail="Доступ только для учителей")
    return user

def require_student(current_user = Depends(get_current_user)):
    user, user_type = current_user
    if user_type != settings.ROLE_STUDENT:
        raise HTTPException(status_code=403, detail="Доступ только для учеников")
    return user