from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.core.database import get_db
from app.models.classroom import ClassRoom
from app.models.student import Student
from app.models.teacher import Teacher
from app.schemas.classroom import ClassCreateRequest, ClassResponse
from app.schemas.student import StudentsBatchCreateRequest
from app.schemas.teacher import TeacherBatchGenerateRequest
from app.services.admin_service import (
    create_classroom,
    create_teachers_batch,
    delete_classroom,
    delete_student,
    delete_teacher,
    generate_students_for_class,
    get_classroom_by_id,
)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)

@router.get("/teachers")
def get_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).order_by(Teacher.id.desc()).all()


@router.post("/teachers/generate", status_code=status.HTTP_201_CREATED)
def generate_teachers(
    data: TeacherBatchGenerateRequest,
    db: Session = Depends(get_db),
):
    return {"teachers": create_teachers_batch(db, data.count)}


@router.delete("/teachers/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
):
    delete_teacher(db, teacher_id)
    return None

@router.get("/classes", response_model=list[ClassResponse])
def get_classes(db: Session = Depends(get_db)):
    return db.query(ClassRoom).order_by(ClassRoom.name.asc()).all()


@router.post("/classes", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
    data: ClassCreateRequest,
    db: Session = Depends(get_db),
):
    return create_classroom(db, data.name, data.teacher_id)


@router.get("/classes/{class_id}", response_model=ClassResponse)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
):
    return get_classroom_by_id(db, class_id)


@router.delete("/classes/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_class(
    class_id: int,
    db: Session = Depends(get_db),
):
    delete_classroom(db, class_id)
    return None


@router.get("/classes/{class_id}/students")
def get_class_students(
    class_id: int,
    db: Session = Depends(get_db),
):
    return db.query(Student).filter(Student.class_id == class_id).order_by(Student.id.asc()).all()

@router.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).order_by(Student.id.desc()).all()


@router.post("/students/generate", status_code=status.HTTP_201_CREATED)
def generate_students(
    data: StudentsBatchCreateRequest,
    db: Session = Depends(get_db),
):
    return generate_students_for_class(db, data.class_name, data.count)


@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    delete_student(db, student_id)
    return None