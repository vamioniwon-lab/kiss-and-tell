from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import Settings
from .database import Base, engine
from .auth import router as auth_router
from .confession import router as confession_router
from .utils.docs import custom_openapi

settings = Settings()

app = FastAPI(title="Kiss and Tell", version="1.0.0", description="API for anonymous confession app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(confession_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome to Kiss & Tell API"}

app.openapi = lambda: custom_openapi(app)
