from fastapi import FastAPI
from app.auth import router as auth_router
from app.database import create_db

app = FastAPI(title="Kiss & Tell API")

create_db()

@app.get("/")
def read_root():
    return {"status": "Backend Running"}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
