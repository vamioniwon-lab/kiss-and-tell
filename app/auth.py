from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from pydantic import BaseModel, EmailStr

from app.database import get_db
from app.models import User

SECRET_KEY = "THIS_IS_YOUR_SECRET_KEY"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------- SCHEMAS ------------- #
class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ------------- HELPERS ------------- #
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# ------------- ENDPOINTS ------------- #
@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = hash_password(data.password)

    user = User(email=data.email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "signup ok", "email": user.email}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = jwt.encode({"email": user.email}, SECRET_KEY, algorithm=ALGORITHM)

    return {"message": "login ok", "token": token}
