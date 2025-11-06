from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from . import models
from .auth import router as auth_router

app = FastAPI(title="Kiss & Tell API", version="1.0.0")

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables once (no duplicate metadata)
Base.metadata.create_all(bind=engine, checkfirst=True)

@app.get("/")
def root():
    return {"status": "ok"}

# Routers
app.include_router(auth_router)
