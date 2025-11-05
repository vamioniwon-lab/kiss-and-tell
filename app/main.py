from fastapi import FastAPI
from .auth import router as auth_router   # ← relative import is safest inside a package

app = FastAPI(title="Kiss & Tell API")

@app.get("/")
def read_root():
    return {"status": "Backend Running"}

# register routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# --- TEMP DEBUG: list all routes so we can verify the router got in ---
from fastapi.routing import APIRoute
@app.get("/_debug/routes")
def list_routes():
    return [{"path": r.path, "name": r.name} for r in app.routes]
