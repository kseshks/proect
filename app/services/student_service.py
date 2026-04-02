from typing import cast

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import Test
from app.models.student import Student
from app.models.test_result import TestResult
from app.core.security import get_password_hash
from app.services.student_generation_service import generate_login, generate_password, generate_student_number

def create_students_batch(db: Session, count: int) -> dict:
    created_students = []
    for _ in range(count):
        login = generate_login()
        password = generate_password(length=10)
        student_number = generate_student_number()

        while db.query(Student).filter(Student.login == login).first():
            login = generate_login()
        while db.query(Student).filter(Student.student_number == student_number).first():
            student_number = generate_student_number()

        db_student = Student(
            login=login,
            student_number=student_number,
            hashed_password=get_password_hash(password)
        )
        db.add(db_student)
        created_students.append({
            "login": login,
            "password": password,
            "student_number": student_number
        })

    db.commit()
    return {
        "message": f"Успешно создано {count} учеников",
        "students": created_students
    }

def get_student_by_id(db: Session, student_id: int) -> Student:
    student: Student | None = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ученик с ID {student_id} не найден"
        )
    return student

def get_all_students(db: Session) -> list[Student]:
    return cast(list[Student], db.query(Student).all())

def delete_student(db: Session, student_id: int) -> None:
    student = get_student_by_id(db, student_id)
    db.delete(student)
    db.commit()

def get_student_results(db: Session, student_id: int) -> list[dict]:
    results = db.query(TestResult).filter(TestResult.student_id == student_id).all()
    return [
        {
            "test_title": r.test.title,
            "total_points": r.total_points,
            "max_points": r.max_points,
            "result": f"{r.total_points}/{r.max_points}"
        }
        for r in results
    ]

def get_students_ratings(db: Session) -> dict:
    tests = db.query(Test).all()
    tests_ratings = []
    for test in tests:
        results = db.query(TestResult).filter(TestResult.test_id == test.id).all()
        test_results = []
        for result in results:
            student = db.query(Student).filter(Student.id == result.student_id).first()
            if student:
                test_results.append({
                    "student_number": student.student_number,
                    "total_points": result.total_points,
                    "max_points": result.max_points,
                    "result": f"{result.total_points}/{result.max_points}",
                })
        tests_ratings.append({
            "test_id": test.id,
            "test_title": test.title,
            "results": test_results
        })
    return {"tests": tests_ratings}