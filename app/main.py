from fastapi import FastAPI
from app.auth import router as auth_router
from app.database import Base, engine

# ✅ Make sure DB tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
