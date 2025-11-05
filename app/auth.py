from fastapi import APIRouter

router = APIRouter()

@router.post("/signup")
def signup():
    return {"ok": True, "route": "signup"}

@router.post("/login")
def login():
    return {"ok": True, "route": "login"}
