from fastapi import FastAPI
from .database import create_tables
from .auth import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")

create_tables()
