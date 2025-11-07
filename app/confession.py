# app/confession.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Confession
from .schemas import ConfessionRequest

router = APIRouter()

@router.post("/confession")
def create_confession(payload: ConfessionRequest, db: Session = Depends(get_db)):
    new = Confession(content=payload.content)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.get("/confession")
def get_all(db: Session = Depends(get_db)):
    return db.query(Confession).all()
