from typing import cast

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import (
    ClassRoom,
    Section,
    SectionAssignment,
    Student,
    Topic,
)


def get_teacher_section_or_404(db: Session, teacher_id: int, section_id: int) -> Section:
    section = db.query(Section).filter(
        Section.id == section_id,
        Section.teacher_id == teacher_id
    ).first()

    if not section:
        raise HTTPException(status_code=404, detail="Раздел не найден")

    return cast(Section, section)


def get_teacher_sections(db: Session, teacher_id: int) -> list[Section]:
    return cast(
        list[Section],
        db.query(Section)
        .filter(Section.teacher_id == teacher_id)
        .order_by(Section.id.desc())
        .all()
    )


def create_section(
    db: Session,
    teacher_id: int,
    title: str,
    description: str | None
) -> Section:
    section = Section(
        title=title,
        description=description,
        teacher_id=teacher_id
    )
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


def delete_section(db: Session, teacher_id: int, section_id: int) -> None:
    section = get_teacher_section_or_404(db, teacher_id, section_id)
    db.delete(section)
    db.commit()


def get_section_topics(db: Session, teacher_id: int, section_id: int) -> list[Topic]:
    section = get_teacher_section_or_404(db, teacher_id, section_id)

    return cast(
        list[Topic],
        db.query(Topic)
        .filter(Topic.section_id == section.id)
        .order_by(Topic.id.desc())
        .all()
    )


def create_topic_in_section(
    db: Session,
    teacher_id: int,
    section_id: int,
    title: str,
    description: str | None
) -> Topic:
    section = get_teacher_section_or_404(db, teacher_id, section_id)

    topic = Topic(
        title=title,
        description=description,
        teacher_id=teacher_id,
        section_id=section.id
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def assign_section(
    db: Session,
    teacher,
    section_id: int,
    class_ids: list[int],
    student_numbers: list[str]
) -> dict:
    section = get_teacher_section_or_404(db, teacher.id, section_id)

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
        students = db.query(Student).join(
            ClassRoom,
            Student.class_id == ClassRoom.id
        ).filter(
            Student.student_number.in_(student_numbers),
            ClassRoom.teacher_id == teacher.id
        ).all()

        for student in students:
            student_ids.add(student.id)

    if not student_ids:
        raise HTTPException(status_code=400, detail="Не выбраны ученики или классы")

    created = 0

    for student_id in student_ids:
        exists = db.query(SectionAssignment).filter(
            SectionAssignment.section_id == section.id,
            SectionAssignment.student_id == student_id
        ).first()

        if exists:
            continue

        assignment = SectionAssignment(
            section_id=section.id,
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