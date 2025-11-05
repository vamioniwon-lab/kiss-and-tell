from fastapi import FastAPI
from .auth import router as auth_router
from .posts import router as posts_router
from .database import Base, engine

app = FastAPI(title="Kiss & Tell API")

# create tables (simple bootstrap)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"status": "Backend Running"}

# register routers
app.include_router(auth_router)
app.include_router(posts_router)
