from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from .settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return pwd_context.hash(p)

def verify_password(p: str, hashed: str) -> bool:
    return pwd_context.verify(p, hashed)

def create_access_token(sub: str, expires_minutes: int | None = None) -> str:
    settings = get_settings()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": sub, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
