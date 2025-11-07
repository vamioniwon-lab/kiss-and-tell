from fastapi import FastAPI
from .database import Base, engine
from .auth import router as auth_router
from .confession import router as conf_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(conf_router, prefix="/confessions", tags=["confessions"])


@app.get("/")
def root():
    return {"message": "Kiss & Tell API running ✅"}
