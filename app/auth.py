from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/signup")
def signup(payload: SignupRequest):
    return {
        "message": "signup ok",
        "username": payload.username,
        "email": payload.email
    }

@router.post("/login")
def login(payload: LoginRequest):
    return {
        "message": "login ok",
        "username": payload.username
    }
