from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine, Base

router = APIRouter(tags=["Maintenance"])

@router.post("/__migrate/add-password")
def add_password_column():
    # Add the column if it doesn't exist, set a temporary default for existing rows
    with engine.begin() as conn:
        conn.execute(text(
            "ALTER TABLE users "
            "ADD COLUMN IF NOT EXISTS password VARCHAR NOT NULL DEFAULT 'temp';"
        ))
        # Optional: drop the default afterwards so future inserts must provide a value
        conn.execute(text("ALTER TABLE users ALTER COLUMN password DROP DEFAULT;"))
    return {"status": "✅ users.password added (or already existed)"}
