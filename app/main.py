from fastapi import FastAPI
from app.database import Base, engine
from app import models  # <-- IMPORTANT: ensures models are registered
from app.auth import router as auth_router
from app.reset_db import router as reset_router

# Create tables (no-ops if they already exist, but DOESN'T change columns)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI", version="0.1.0")

app.include_router(auth_router)
app.include_router(reset_router)

@app.get("/")
def root():
    return {"ok": True}
