from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class ClassRoom(Base):
    __tablename__ = 'classrooms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=True)

    teacher = relationship("Teacher", back_populates="classes")
    students = relationship("Student", back_populates="classroom")