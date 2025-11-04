from fastapi import FastAPI
from .auth import router as auth_router

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Backend Running"}

# ✅ register routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
