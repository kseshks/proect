from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_teacher
from app.core.database import get_db
from app.schemas.classroom import ClassCreateRequest, ClassResponse  # ← ВОТ ЭТО ДОБАВИТЬ
from app.schemas.student import TeacherStudentsGenerateRequest
from app.schemas.topic import (
    MaterialLinkCreateRequest,
    QuestionsBatchCreateRequest,
    TopicCreateRequest,
    TopicResponse,
    TopicUpdateRequest,
    AssignTopicRequest,
)
from app.services.teacher_service import (
    add_file_material,
    add_link_material,
    add_topic_questions,
    create_topic,
    delete_topic,
    get_teacher_class_students,
    get_teacher_classes,
    get_teacher_topic_or_404,
    get_topic_questions,
    update_topic,
    get_teacher_topics,
    assign_topic,
    generate_students_for_teacher_class,
    create_classroom_for_teacher,
    delete_classroom_for_teacher,
    delete_student_for_teacher,
    get_teacher_topic_materials,
    delete_material,
    delete_question,
)

router = APIRouter(prefix="/teacher", tags=["teacher"])


@router.get("/ratings/students")
def teacher_students_rating(teacher=Depends(require_teacher)):
    return {"items": [], "total": 0}


@router.get("/classes")
def teacher_classes(db: Session = Depends(get_db), teacher=Depends(require_teacher)):
    return get_teacher_classes(db, teacher.id)


@router.post("/classes", status_code=status.HTTP_201_CREATED)
def teacher_create_class(
    data: ClassCreateRequest,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    return create_classroom_for_teacher(db, teacher.id, data.name)


@router.delete("/classes/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def teacher_delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    delete_classroom_for_teacher(db, teacher.id, class_id)
    return None


@router.get("/classes/{class_id}/students")
def teacher_class_students(class_id: int, db: Session = Depends(get_db), teacher=Depends(require_teacher)):
    return get_teacher_class_students(db, teacher.id, class_id)


@router.post("/classes/{class_id}/students/generate", status_code=status.HTTP_201_CREATED)
def teacher_generate_students(
    class_id: int,
    data: TeacherStudentsGenerateRequest,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    return generate_students_for_teacher_class(db, teacher.id, class_id, data.count)


@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def teacher_delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    delete_student_for_teacher(db, teacher.id, student_id)
    return None


@router.get("/topics", response_model=list[TopicResponse])
def teacher_topics(db: Session = Depends(get_db), teacher=Depends(require_teacher)):
    return get_teacher_topics(db, teacher.id)


@router.post("/topics", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def teacher_create_topic(
    data: TopicCreateRequest,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    return create_topic(db, teacher.id, data.title, data.description)


@router.get("/topics/{topic_id}", response_model=TopicResponse)
def teacher_topic(topic_id: int, db: Session = Depends(get_db), teacher=Depends(require_teacher)):
    return get_teacher_topic_or_404(db, teacher.id, topic_id)


@router.put("/topics/{topic_id}", response_model=TopicResponse)
def teacher_update_topic(
    topic_id: int,
    data: TopicUpdateRequest,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    return update_topic(db, teacher.id, topic_id, data.model_dump(exclude_unset=True))


@router.delete("/topics/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def teacher_delete_topic(topic_id: int, db: Session = Depends(get_db), teacher=Depends(require_teacher)):
    delete_topic(db, teacher.id, topic_id)
    return None


@router.get("/topics/{topic_id}/materials")
def teacher_topic_materials(
    topic_id: int,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    return get_teacher_topic_materials(db, teacher.id, topic_id)


@router.post("/topics/{topic_id}/materials/link", status_code=status.HTTP_201_CREATED)
def teacher_add_link(
    topic_id: int,
    data: MaterialLinkCreateRequest,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    return add_link_material(db, teacher.id, topic_id, data.title, data.url)


@router.post("/topics/{topic_id}/materials/file", status_code=status.HTTP_201_CREATED)
def teacher_add_file(
    topic_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    return add_file_material(db, teacher.id, topic_id, file)


@router.delete("/materials/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def teacher_delete_material(
    material_id: int,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    delete_material(db, teacher.id, material_id)
    return None


@router.get("/topics/{topic_id}/questions")
def teacher_questions(topic_id: int, db: Session = Depends(get_db), teacher=Depends(require_teacher)):
    return get_topic_questions(db, teacher.id, topic_id)


@router.post("/topics/{topic_id}/questions", status_code=status.HTTP_201_CREATED)
def teacher_add_questions(
    topic_id: int,
    data: QuestionsBatchCreateRequest,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    return add_topic_questions(
        db,
        teacher.id,
        topic_id,
        [q.model_dump() for q in data.questions]
    )


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def teacher_delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    delete_question(db, teacher.id, question_id)
    return None


@router.post("/topics/{topic_id}/assign")
def teacher_assign_topic(
    topic_id: int,
    data: AssignTopicRequest,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    return assign_topic(db, teacher, topic_id, data.class_ids, data.student_numbers)

@router.get("/topics/{topic_id}/assignments")
def teacher_topic_assignments(
    topic_id: int,
    db: Session = Depends(get_db),
    teacher=Depends(require_teacher)
):
    from app.services.teacher_service import get_topic_assignments
    return get_topic_assignments(db, teacher.id, topic_id)