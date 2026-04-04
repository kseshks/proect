from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    student_number = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)

    classroom = relationship("ClassRoom", back_populates="students")
    assignments = relationship("TopicAssignment", back_populates="student", cascade="all, delete-orphan")
    dialog_messages = relationship("TopicDialogMessage", back_populates="student", cascade="all, delete-orphan")