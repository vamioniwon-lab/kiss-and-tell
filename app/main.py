from fastapi import FastAPI
from app.auth import router as auth_router

app = FastAPI(title="Kiss & Tell API")

@app.get("/")
def read_root():
    return {"status": "Backend Running"}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
