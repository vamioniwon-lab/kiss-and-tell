from fastapi import APIRouter
from app.database import engine, Base
from sqlalchemy import text

router = APIRouter()

@router.post("/__reset/all")
def reset_all():
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
    Base.metadata.create_all(bind=engine)
    return {"status": "✅ Database reset successfully"}
