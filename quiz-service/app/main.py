import logging
import sys

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import settings
from app.quiz.router import router as quiz_router

# ── Logging ────────────────────────────────────────────────────────────────────

logging.basicConfig(
    stream=sys.stdout,
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

# ── Application ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="DailyLearn Quiz Service",
    version="0.1.0",
    description="Generates quizzes from learning card conspects using a local LLM (Ollama).",
)

app.include_router(quiz_router, prefix="/api/v1")


@app.get("/health", tags=["ops"])
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})
