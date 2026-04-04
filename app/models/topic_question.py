from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class TopicQuestion(Base):
    __tablename__ = 'topic_questions'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    text = Column(String, nullable=False)

    topic = relationship("Topic", back_populates="questions")
    dialog_messages = relationship("TopicDialogMessage", back_populates="question")