
from fastapi import FastAPI
from .database import Base, engine
from .auth import router as auth_router
from .models import *  # noqa: F401

# Auto-create tables (simple for MVP; migrations can come later)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kiss & Tell API", version="1.0")

@app.get("/")
def read_root():
    return {"status": "Backend Running"}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
