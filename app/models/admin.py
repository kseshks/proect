from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)