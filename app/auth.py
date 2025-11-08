from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate
from app.utils.password import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    new_user = User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "email": new_user.email}
