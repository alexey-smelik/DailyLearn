from fastapi import FastAPI

from app.api import api_router

app = FastAPI(title="DailyLearn API", version="0.1.0")

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
