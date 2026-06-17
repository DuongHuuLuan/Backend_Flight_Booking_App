from sqlalchemy import Column, Integer, DateTime, String

from app.infrastructure.database.base import Base


class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    country = Column(String(100))
    city = Column(String(100))
    password = Column(String(100))
    avatar = Column(String(255))
    created_at = Column(DateTime)