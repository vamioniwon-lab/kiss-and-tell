from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Confession
from .schemas import ConfessionRequest, ConfessionResponse

router = APIRouter(prefix="/confession", tags=["Confession"])

@router.post("/", response_model=ConfessionResponse)
def create_confession(payload: ConfessionRequest, db: Session = Depends(get_db)):
    confession = Confession(content=payload.content, owner_id=1)   # future = JWT
    db.add(confession)
    db.commit()
    db.refresh(confession)
    return confession

@router.get("/", response_model=list[ConfessionResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(Confession).all()

@router.get("/{confession_id}", response_model=ConfessionResponse)
def get_one(confession_id: int, db: Session = Depends(get_db)):
    confession = db.query(Confession).filter(Confession.id == confession_id).first()
    if not confession:
        raise HTTPException(status_code=404, detail="Not found")
    return confession
