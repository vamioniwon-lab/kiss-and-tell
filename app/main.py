from fastapi import FastAPI
from app.database import engine, Base
from app.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
from app.reset_db import router as reset_router
app.include_router(reset_router)
