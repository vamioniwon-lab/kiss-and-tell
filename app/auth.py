from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from .database import get_db
from .models import User
from .utils import hash_password, verify_password, create_access_token

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == user.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    found = db.query(User).filter(User.email == user.email).first()
    if not found:
        raise HTTPException(status_code=401, detail="invalid credentials")

    if not verify_password(user.password, found.hashed_password):
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_access_token({"id": found.id, "email": found.email})

    return {"access_token": token, "token_type": "bearer"}
