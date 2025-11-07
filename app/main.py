from fastapi import FastAPI
from app.database import Base, engine
from app import models                   # <-- import models so tables are registered
from app.auth import router as auth_router
from app.reset_db import router as reset_router

app = FastAPI()

# create tables if they don't exist
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(reset_router)
