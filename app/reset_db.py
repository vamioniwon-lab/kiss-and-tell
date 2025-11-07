from fastapi import APIRouter
from app.database import Base, engine
from app.models import User

router = APIRouter(tags=["Maintenance"])

@router.post("/__reset/users")
def reset_users():
    # Drop and recreate ONLY the 'users' table
    Base.metadata.drop_all(bind=engine, tables=[User.__table__], checkfirst=True)
    Base.metadata.create_all(bind=engine, tables=[User.__table__])
    return {"status": "reset-done"}
