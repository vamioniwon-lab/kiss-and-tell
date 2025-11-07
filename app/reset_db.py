from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.database import engine

router = APIRouter(prefix="/__reset", tags=["RESET"])

@router.post("/users")
def reset_users():
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS users;"))
    return {"status": "users table dropped"}
