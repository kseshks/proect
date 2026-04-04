from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class TopicMaterial(Base):
    __tablename__ = 'topic_materials'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    material_type = Column(String, nullable=False)
    title = Column(String, nullable=True)
    url = Column(String, nullable=True)
    file_path = Column(String, nullable=True)

    topic = relationship("Topic", back_populates="materials ")
