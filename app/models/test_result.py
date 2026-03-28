from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    total_points = Column(Float, default=0.0)

    student = relationship("Student", back_populates="test_results")
    test = relationship("Test", back_populates="test_results")
    student_answers = relationship("StudentAnswer", back_populates="test_result", cascade="all, delete-orphan")