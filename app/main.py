from fastapi import FastAPI
from app.database import Base, engine
from app.auth import router as auth_router
from app.confession import router as confession_router
from app.maintenance import router as maintenance_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(confession_router, prefix="/confession", tags=["Confession"])
app.include_router(maintenance_router, tags=["Maintenance"])


@app.get("/")
def root():
    return {"status": "ok"}
