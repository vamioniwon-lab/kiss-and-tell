from fastapi import APIRouter
from app.database import engine, Base
from sqlalchemy import text

router = APIRouter()

@router.post("/__reset/all")
def reset_all():
    with engine.connect() as conn:
        # Drop everything
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        # Recreate schema
        conn.execute(text("CREATE SCHEMA public;"))
    Base.metadata.create_all(bind=engine)
    return {"status": "✅ ALL TABLES RESET"}
