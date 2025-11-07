from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .deps import get_db, get_current_user_id
from .schemas import ConfessionRequest, CommentRequest
from .models import Confession, Like, Comment

router = APIRouter(prefix="/confession", tags=["Confession"])

@router.get("/confession/")
def get_all(db: Session = Depends(get_db)):
    items = db.query(Confession).order_by(Confession.id.desc()).all()
    result = []
    for c in items:
        result.append({
            "id": c.id,
            "message": c.message,
            "likes": db.query(Like).filter(Like.confession_id == c.id).count(),
            "comments": db.query(Comment).filter(Comment.confession_id == c.id).count(),
        })
    return result

@router.get("/confession/{confession_id}")
def get_one(confession_id: int, db: Session = Depends(get_db)):
    c = db.query(Confession).filter(Confession.id == confession_id).first()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    comments = db.query(Comment).filter(Comment.confession_id == c.id).order_by(Comment.id.asc()).all()
    return {
        "id": c.id,
        "message": c.message,
        "likes": db.query(Like).filter(Like.confession_id == c.id).count(),
        "comments": [{"id": m.id, "message": m.message} for m in comments],
    }

@router.post("/confession/")
def create(body: ConfessionRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    c = Confession(message=body.message, user_id=user_id)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "message": c.message, "likes": 0, "comments": []}

@router.post("/confession/{confession_id}/like")
def like(confession_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    exists = db.query(Confession).filter(Confession.id == confession_id).first()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    has = db.query(Like).filter(Like.confession_id == confession_id, Like.user_id == user_id).first()
    if has:
        return {"status": "ok", "liked": True}
    db.add(Like(confession_id=confession_id, user_id=user_id))
    db.commit()
    return {"status": "ok", "liked": True}

@router.post("/confession/{confession_id}/comment")
def comment(confession_id: int, body: CommentRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    exists = db.query(Confession).filter(Confession.id == confession_id).first()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    cm = Comment(confession_id=confession_id, user_id=user_id, message=body.message)
    db.add(cm)
    db.commit()
    db.refresh(cm)
    return {"id": cm.id, "message": cm.message}
