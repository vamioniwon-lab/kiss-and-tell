from fastapi import FastAPI
from app.auth import router as auth_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Backend Running"}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
