from fastapi import FastAPI
from .auth import router as auth_router

app = FastAPI(title="Kiss & Tell API")

@app.get("/")
def read_root():
    return {"status": "Backend Running"}

# ✅ Register authentication routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# ✅ Debug route to list all routes
@app.get("/_debug/routes")
def list_routes():
    routes_info = []
    for route in app.routes:
        routes_info.append({"path": route.path, "name": route.name})
    return routes_info
