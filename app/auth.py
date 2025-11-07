from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from .database import get_db
from .models import User
from .schemas import SignupRequest, LoginRequest
from .settings import Settings

router = APIRouter()

settings = Settings()
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_ctx.hash(password)

def verify_password(plain, hashed):
    return pwd_ctx.verify(plain, hashed)

def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=30),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == data.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email exists")

    user = User(email=data.email, password=hash_password(data.password))
    db.add(user)
    db.commit()
    return {"message": "signup ok", "email": user.email}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Bad credentials")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Bad credentials")

    token = create_token(user.id)
    return {"message": "login ok", "token": token}
