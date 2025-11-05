from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# AUTH
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True

# POSTS
class PostCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)

class PostPublic(BaseModel):
    id: int
    content: str
    created_at: datetime
    # author intentionally omitted for anonymity
    class Config:
        from_attributes = True
