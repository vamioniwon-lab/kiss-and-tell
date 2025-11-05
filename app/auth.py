from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils import hash_password, verify_password

router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str
    

@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    # Check if email exists
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(payload.password)
    new_user = User(email=payload.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "signup ok", "email": new_user.email}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "login ok", "email": user.email}
