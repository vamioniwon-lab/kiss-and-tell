# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .auth import router as auth_router
from .confession import router as confession_router

app = FastAPI(
    title="Kiss & Tell API",
    version="1.0.0"
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(confession_router, prefix="/confession", tags=["Confession"])

@app.get("/", tags=["Default"])
def home():
    return {"message": "Kiss & Tell API Running ✅"}
