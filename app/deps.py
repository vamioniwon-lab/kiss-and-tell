from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .auth import decode_token
from .database import get_db
from .models import User
from sqlalchemy import or_

def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split()[-1]
    try:
        data = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    sub = data.get("sub")
    user = db.query(User).filter(or_(User.email==sub, User.phone==sub)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
