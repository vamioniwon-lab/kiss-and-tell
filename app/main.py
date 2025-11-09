from fastapi import FastAPI
from app.auth import router as auth_router
from app.confession import router as confession_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(confession_router)
