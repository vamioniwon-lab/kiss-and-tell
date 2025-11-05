from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db
from .deps import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/create", response_model=schemas.PostPublic)
def create_post(
    payload: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    post = models.Post(content=payload.content, author_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post  # author hidden via schema

@router.get("/list", response_model=List[schemas.PostPublic])
def list_posts(db: Session = Depends(get_db)):
    # return newest first; authors are intentionally not exposed
    return db.query(models.Post).order_by(models.Post.id.desc()).all()
