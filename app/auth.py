
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .database import get_db
from . import schemas, models

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", response_model=schemas.UserOut)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if not payload.email and not payload.phone:
        raise HTTPException(status_code=400, detail="Provide email or phone")

    if payload.email:
        existing = db.query(models.User).filter(models.User.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

    if payload.phone:
        existing = db.query(models.User).filter(models.User.phone == payload.phone).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone already registered")

    hashed = pwd_context.hash(payload.password)
    user = models.User(
        email=payload.email,
        phone=payload.phone,
        password=hashed,
        display_name=payload.display_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if payload.email:
        user = db.query(models.User).filter(models.User.email == payload.email).first()
    elif payload.phone:
        user = db.query(models.User).filter(models.User.phone == payload.phone).first()
    else:
        raise HTTPException(status_code=400, detail="Provide email or phone")

    if not user or not pwd_context.verify(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login ok", "user_id": user.id, "display_name": user.display_name}
