from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import get_db, User

router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    user = User(email=payload.email, password=payload.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "signup ok", "email": user.email}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or user.password != payload.password:
        return {"error": "Invalid login"}

    return {"message": "login ok", "email": user.email}
