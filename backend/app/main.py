from fastapi import FastAPI, Depends

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.projects import router as projects_router
from app.api.v1.commitments import router as commitments_router
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

app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(users_router, prefix=settings.api_v1_prefix)
app.include_router(projects_router, prefix=settings.api_v1_prefix)
app.include_router(commitments_router, prefix=settings.api_v1_prefix)