from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Confession
from app.schemas import ConfessionRequest, ConfessionResponse
from app.deps import get_current_user

router = APIRouter(prefix="/confession")

@router.post("/", response_model=ConfessionResponse)
def create_confession(req: ConfessionRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_conf = Confession(
        user_id=user.id if user else None,
        content=req.content
    )
    db.add(new_conf)
    db.commit()
    db.refresh(new_conf)
    return new_conf

@router.get("/", response_model=list[ConfessionResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(Confession).order_by(Confession.id.desc()).all()

@router.get("/{confession_id}", response_model=ConfessionResponse)
def get_one(confession_id: int, db: Session = Depends(get_db)):
    conf = db.query(Confession).filter(Confession.id == confession_id).first()
    if not conf:
        raise HTTPException(status_code=404, detail="Not found")
    return conf

@router.post("/{confession_id}/like")
def like(confession_id: int, db: Session = Depends(get_db)):
    conf = db.query(Confession).filter(Confession.id == confession_id).first()
    if not conf:
        raise HTTPException(status_code=404, detail="Not found")
    conf.likes += 1
    db.commit()
    return {"message": "liked"}

@router.post("/{confession_id}/comment")
def comment(confession_id: int, db: Session = Depends(get_db)):
    conf = db.query(Confession).filter(Confession.id == confession_id).first()
    if not conf:
        raise HTTPException(status_code=404, detail="Not found")
    conf.comments += 1
    db.commit()
    return {"message": "comment added"}
