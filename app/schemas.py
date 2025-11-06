from pydantic import BaseModel

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ConfessionRequest(BaseModel):
    content: str

class ConfessionResponse(BaseModel):
    id: int
    content: str
    likes: int
    comments: int

    class Config:
        orm_mode = True
