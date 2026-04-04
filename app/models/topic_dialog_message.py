from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class TopicDialogMessage(Base):
    __tablename__ = 'topic_dialog_messages'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('topic_questions.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)

    topic = relationship("Topic", back_populates="dialog_messages")
    student = relationship("Student", back_populates="dialog_messages")
    question = relationship("TopicQuestion", back_populates="dialog_messages")