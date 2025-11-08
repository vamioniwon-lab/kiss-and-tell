from fastapi import APIRouter
from app.database import engine, Base

router = APIRouter(prefix="/__reset", tags=["Maintenance"])

@router.post("/all")
def reset_all():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"status": "✅ Database reset successfully"}
