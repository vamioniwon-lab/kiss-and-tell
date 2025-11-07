from pydantic import BaseModel, EmailStr
from datetime import datetime

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ConfessionRequest(BaseModel):
    content: str

class ConfessionResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True
