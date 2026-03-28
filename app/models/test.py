from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)

    teacher = relationship("Teacher", back_populates="tests")
    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan")
    results = relationship("TestResult", back_populates="test", cascade="all, delete-orphan")