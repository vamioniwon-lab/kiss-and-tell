from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.deps import get_db
from app.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_ctx = CryptContext(schemes=["argon2"], deprecated="auto")

class UserCreate(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed = pwd_ctx.hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    return {"id": new_user.id, "email": new_user.email}
