from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, model_validator
from typing import Optional


router = APIRouter()


# ✅ SIGNUP REQUEST MODEL
class SignupRequest(BaseModel):
    email: str
    password: str


# ✅ SIGNUP ROUTE
@router.post("/signup")
def signup(payload: SignupRequest):
    return {
        "message": "signup ok",
        "email": payload.email
    }


# ✅ LOGIN REQUEST MODEL (supports username or email)
class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def validate_identifier(self):
        if not self.username and not self.email:
            raise ValueError("Either 'username' or 'email' is required.")
        return self


# ✅ LOGIN ROUTE
@router.post("/login")
def login(payload: LoginRequest):
    identifier = payload.username or payload.email
    return {
        "message": "login ok",
        "identifier": identifier
    }
