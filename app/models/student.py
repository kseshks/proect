from sqlalchemy import Column, Integer
from sqlparse.tokens import String

from app.core.database import Base


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    hashed_password = Column(String, nullable=False)
    student_number = Column(Integer, nullable=False, unique=True)