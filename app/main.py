from fastapi import FastAPI
from app.database import engine, Base
from app.auth import router as auth_router
from app.maintenance import router as maintenance_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ROUTES
app.include_router(auth_router)
app.include_router(maintenance_router)

@app.get("/")
def root():
    return {"message": "Kiss & Tell API is live"}
