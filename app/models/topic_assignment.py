from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class TopicAssignment(Base):
    __tablename__ = 'topic_assignments'
    __table_args__ = (
        UniqueConstraint("topic_id", "student_id", name="uq_topic_student_assignment"),
    )
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    assigned_by_teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    topic = relationship("Topic", back_populates="assignments")
    student = relationship("Student", back_populates="assignments")