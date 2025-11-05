from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.schemas import SignupRequest, LoginRequest
from app.database import SessionLocal, User, create_db

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# create DB if not exist
create_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(raw, hashed):
    return pwd_context.verify(raw, hashed)


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == payload.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    existing_username = db.query(User).filter(User.username == payload.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(payload.password)

    user = User(username=payload.username, email=payload.email, password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "signup ok", "id": user.id}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "login ok", "username": user.username}
