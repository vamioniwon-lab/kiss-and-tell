from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app import schemas, models

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", response_model=schemas.UserOut)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):

    if not payload.email and not payload.phone:
        raise HTTPException(status_code=400, detail="Email or phone is required")

    if payload.email:
        existing = db.query(models.User).filter(models.User.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    if payload.phone:
        existing = db.query(models.User).filter(models.User.phone == payload.phone).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone already exists")

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
        raise HTTPException(status_code=400, detail="Email or phone required")

    if not user or not pwd_context.verify(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": user.id}
