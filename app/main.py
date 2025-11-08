from fastapi import FastAPI
from app.auth import router as auth_router
from app.maintenance import router as maintenance_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(maintenance_router)
