from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    teacher = relationship("Teacher", back_populates="sections")
    topics = relationship("Topic", back_populates="section", cascade="all, delete-orphan")
    assignments = relationship("SectionAssignment", back_populates="section", cascade="all, delete-orphan")