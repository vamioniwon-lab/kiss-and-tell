from fastapi import FastAPI
from app.database import Base, engine
from app.auth import router as auth_router
from app.models import *

# ✅ Create DB tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
