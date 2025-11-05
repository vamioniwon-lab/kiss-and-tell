from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# ✅ MODELS
class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# ✅ ROUTES
@router.post("/signup")
def signup(payload: SignupRequest):
    return {
        "message": "signup ok",
        "email": payload.email
    }

@router.post("/login")
def login(payload: LoginRequest):
    return {
        "message": "login ok",
        "email": payload.email
    }
