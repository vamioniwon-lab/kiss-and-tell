from fastapi import FastAPI
from database import engine, Base
from auth import router as auth_router
from maintenance import router as maintenance_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ROUTES
app.include_router(auth_router)
app.include_router(maintenance_router)


@app.get("/")
def root():
    return {"message": "Kiss & Tell API is running!"}
