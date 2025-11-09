from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.models import User
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "kiss-and-tell-secret"
ALGORITHM = "HS256"


# ------------------------------
# SCHEMAS
# ------------------------------
class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# password hash
def hash_password(password: str):
    # bcrypt only allows 72 bytes max
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    plain = plain[:72]
    return pwd_context.verify(plain, hashed)


# create JWT
def create_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(days=3)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# SIGNUP
@router.post("/signup")
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    email = payload.email
    password = payload.password

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=email,
        password=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_token({"user_id": new_user.id})
    return {"token": token}


# LOGIN
@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    email = payload.email
    password = payload.password

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": user.id})
    return {"token": token}
