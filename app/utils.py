# app/utils.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "secret"
ALGO = "HS256"

def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd.verify(password, hashed)

def create_token(data: dict, expires_mins: int = 60):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=expires_mins)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
