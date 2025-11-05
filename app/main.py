from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(payload: SignupRequest):
    return {
        "message": "signup ok",
        "email": payload.email
    }


class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(payload: LoginRequest):
    return {
        "message": "login ok",
        "email": payload.email
    }
