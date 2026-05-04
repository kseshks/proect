from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class SectionAssignment(Base):
    __tablename__ = "section_assignments"
    __table_args__ = (
        UniqueConstraint("section_id", "student_id", name="uq_section_student_assignment"),
    )

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    assigned_by_teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    section = relationship("Section", back_populates="assignments")
    student = relationship("Student", back_populates="section_assignments")