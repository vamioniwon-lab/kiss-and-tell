from fastapi import FastAPI
from app.database import create_tables
from app.auth import router as auth_router
from app.confession import router as confession_router

app = FastAPI()

create_tables()

app.include_router(auth_router)
app.include_router(confession_router)

@app.get("/")
def root():
    return {"status": "running"}
