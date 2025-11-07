from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Confession(Base):
    __tablename__ = "confessions"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    likes = relationship("Like", back_populates="confession", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="confession", cascade="all, delete-orphan")

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    confession_id = Column(Integer, ForeignKey("confessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    confession = relationship("Confession", back_populates="likes")
    __table_args__ = (UniqueConstraint("confession_id", "user_id", name="uq_confession_user_like"),)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    confession_id = Column(Integer, ForeignKey("confessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    confession = relationship("Confession", back_populates="comments")
