from fastapi import APIRouter
from sqlalchemy import text
from app.core.db import engine

router = APIRouter()

@router.get("/status")
def status():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "down"
    return {"status": "ok", "db": db_status}
