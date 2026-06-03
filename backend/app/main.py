from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
)


@app.get("/")
async def healthcheck():
    return {
        "status": "ok",
        "service": settings.app_name,
    }