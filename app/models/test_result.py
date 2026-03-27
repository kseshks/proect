from sqlalchemy import Column, Integer, ForeignKey

from app.core.database import Base


class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, ForeignKey('answers.id'))
