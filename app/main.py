from fastapi import FastAPI
from auth import router as auth_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Backend Running"}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
