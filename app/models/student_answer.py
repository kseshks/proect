from sqlalchemy import Column, Integer, ForeignKey, Boolean, Float, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class StudentAnswer(Base):
    __tablename__ = 'student_answers'

    id = Column(Integer, primary_key=True)
    test_result_id = Column(Integer, ForeignKey("test_results.id"), nullable=False)

    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    points_earned = Column(Float, default=0.0)

    test_result = relationship("TestResult", back_populates="student_answers")
    question = relationship("Question", back_populates="student_answers")