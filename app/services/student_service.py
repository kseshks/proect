from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentRegistrationResponse
from app.core.security import get_password_hash
from app.services.student_generation_service import generate_login, generate_password, generate_student_number


def create_student(db: Session) -> StudentRegistrationResponse:
    login = generate_login()
    password = generate_password(length=10)
    student_number = generate_student_number()

    existing = db.query(Student).filter(Student.login == login).first()
    if existing:
        login = generate_login()

    existing_number = db.query(Student).filter(Student.student_number == student_number).first()
    if existing_number:
        student_number = generate_student_number()

    db_student = Student(
        login=login,
        student_number=student_number,
        hashed_password=get_password_hash(password)
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return StudentRegistrationResponse(
        login=login,
        student_number=student_number,
        password=password,
        message="Ученик успешно создан"
    )