from fastapi import FastAPI
from .auth import router as auth_router
from .database import create_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(auth_router, prefix="/auth")
