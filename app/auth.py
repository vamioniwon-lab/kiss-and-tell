from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from app.database import get_db
from app.models import User
from app.schemas import SignupRequest, LoginRequest

router = APIRouter(prefix="/auth")
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = "TEST_SECRET"

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email exists")

    new_user = User(
        email=data.email,
        password=pwd.hash(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "signup ok", "email": data.email}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not pwd.verify(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = jwt.encode({"id": user.id}, SECRET, algorithm="HS256")
    return {"message": "login ok", "token": token}
