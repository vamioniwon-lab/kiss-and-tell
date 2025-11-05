from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

from . import models
from .deps import get_db

router = APIRouter()

SECRET_KEY = "MY_SUPER_SECRET_KEY"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MODELS
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=6)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup")
def signup(body: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()

    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        email=body.email,
        password=hash_password(body.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "signup ok", "email": new_user.email}


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(body.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user.email
    }
