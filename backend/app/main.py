from fastapi import FastAPI, Depends

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.dependencies import get_db


app = FastAPI(
    title=settings.app_name,
)


@app.get("/")
async def healthcheck():
    return {
        "status": "ok",
        "service": settings.app_name,
    }

@app.get("/db-health")
def db_health(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "database": "ok",
    }