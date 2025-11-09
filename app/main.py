from fastapi import Depends
from fastapi import FastAPI
from app.database import get_db
from app.auth import router as auth_router
from app.confession import router as confession_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(confession_router)
from sqlalchemy import text

@app.post("/__migrate/confessions")
def migrate_confessions(db = Depends(get_db)):
    try:
        db.execute(text("ALTER TABLE confessions ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()"))
        db.execute(text("ALTER TABLE confessions ADD COLUMN IF NOT EXISTS user_id INTEGER"))
        db.commit()
        return {"status": "confessions table updated"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
