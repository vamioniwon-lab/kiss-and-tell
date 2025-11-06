from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os

from . import models
from .deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_SUPER_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_HOURS = 6

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- Schemas ----
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: EmailStr

# ---- Utils ----
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_HOURS)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---- Routes ----
@router.post("/signup")
def signup(body: SignupRequest, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.email == body.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(email=body.email, password=hash_password(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "signup ok", "email": user.email}

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()
    if not user or not verify_password(body.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    token = create_token({"sub": user.email})
    return TokenResponse(access_token=token, email=user.email)
