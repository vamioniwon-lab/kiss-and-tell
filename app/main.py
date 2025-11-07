from fastapi import FastAPI
from app.database import Base, engine
from app.auth import router as auth_router
from app.reset_db import router as reset_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(reset_router)


@app.get("/")
def root():
    return {"message": "Kiss & Tell API Running ✅"}
