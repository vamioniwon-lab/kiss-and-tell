from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), unique=True, index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), default="Anonymous")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    age: Mapped[int] = mapped_column(Integer, default=18)
    location: Mapped[str] = mapped_column(String(120), default="")
    bio: Mapped[str] = mapped_column(Text, default="")
    intentions: Mapped[str] = mapped_column(String(240), default="")
    trust: Mapped[float] = mapped_column(Float, default=3.0)
    photo_url: Mapped[str] = mapped_column(String(400), default="")

class Pact(Base):
    __tablename__ = "pacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    user_a_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_b_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    when: Mapped[str] = mapped_column(String(64), default="")
    where: Mapped[str] = mapped_column(String(200), default="")
    note: Mapped[str] = mapped_column(String(500), default="")
    status: Mapped[str] = mapped_column(String(32), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Gift(Base):
    __tablename__ = "gifts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pact_code: Mapped[str] = mapped_column(String(16), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipient_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    amount: Mapped[str] = mapped_column(String(64))
    method: Mapped[str] = mapped_column(String(32), default="Wallet")
    status: Mapped[str] = mapped_column(String(32), default="escrow")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Proof(Base):
    __tablename__ = "proofs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pact_code: Mapped[str] = mapped_column(String(16), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    visibility: Mapped[str] = mapped_column(String(16), default="private")
    image_path: Mapped[str] = mapped_column(String(400))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Story(Base):
    __tablename__ = "stories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pact_code: Mapped[str] = mapped_column(String(16), default="")
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category: Mapped[str] = mapped_column(String(64), default="Chaotic")
    location: Mapped[str] = mapped_column(String(120), default="")
    text: Mapped[str] = mapped_column(Text)
    anon: Mapped[bool] = mapped_column(Boolean, default=True)
    ratings: Mapped[str] = mapped_column(String(64), default="4,4,4")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Reaction(Base):
    __tablename__ = "reactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(ForeignKey("stories.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    kind: Mapped[str] = mapped_column(String(24))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
