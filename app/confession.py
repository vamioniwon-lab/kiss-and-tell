from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .models import Confession

router = APIRouter()

class ConfessionSchema(BaseModel):
    title: str
    body: str


@router.post("/")
def create_confession(payload: ConfessionSchema, db: Session = Depends(get_db)):
    c = Confession(title=payload.title, body=payload.body)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.get("/")
def get_confessions(db: Session = Depends(get_db)):
    return db.query(Confession).all()
