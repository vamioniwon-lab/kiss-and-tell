from fastapi import FastAPI
from .database import Base, engine
from .auth import router as auth_router
from .confession import router as confession_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(confession_router)

@app.get("/")
def home():
    return {"message": "kiss-and-tell API ready ✅"}
