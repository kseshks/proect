from sqlalchemy import Integer, Column, String, Text, Float, ForeignKey

from app.core.database import Base


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    test_id = Column(Integer, ForeignKey('tests.id'))
    question_type = Column(String)
    points = Column(Float, nullable=False, default=1.0)