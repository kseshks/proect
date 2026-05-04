from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)

    teacher = relationship("Teacher", back_populates="topics")
    section = relationship("Section", back_populates="topics")

    materials = relationship("TopicMaterial", back_populates="topic", cascade="all, delete-orphan")
    questions = relationship("TopicQuestion", back_populates="topic", cascade="all, delete-orphan")
    assignments = relationship("TopicAssignment", back_populates="topic", cascade="all, delete-orphan")
    dialog_messages = relationship("TopicDialogMessage", back_populates="topic", cascade="all, delete-orphan")