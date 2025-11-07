from sqlalchemy import Column, Integer, String, DateTime, Text, func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Confession(Base):
    __tablename__ = "confessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
