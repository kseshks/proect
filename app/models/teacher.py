from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    classes = relationship("ClassRoom", back_populates="teacher")
    topics = relationship("Topic", back_populates="teacher", cascade="all, delete-orphan")