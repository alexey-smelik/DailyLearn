"""HTTP clients for web-api and quiz-service."""

import httpx

from app.config import settings


async def toggle_card(card_id: str) -> dict:
    """POST /api/v1/learning-cards/{card_id}/toggle and return the response JSON."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            f"{settings.web_api_url}/api/v1/learning-cards/{card_id}/toggle"
        )
        response.raise_for_status()
        return response.json()


async def skip_card(card_id: str) -> None:
    """POST /api/v1/learning-cards/{card_id}/skip — record iteration without sending."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            f"{settings.web_api_url}/api/v1/learning-cards/{card_id}/skip"
        )
        response.raise_for_status()


async def save_conspect(card_id: str, conspect: str) -> None:
    """POST /api/v1/learning-cards/{card_id}/save-conspect — save user's study notes."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            f"{settings.web_api_url}/api/v1/learning-cards/{card_id}/save-conspect",
            json={"conspect": conspect},
        )
        response.raise_for_status()


async def generate_quiz(card_id: str, num_questions: int = 3) -> dict:
    """POST /api/v1/quiz/generate/from-card/{card_id} — generate a quiz from card's conspect."""
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{settings.quiz_service_url}/api/v1/quiz/generate/from-card/{card_id}",
            json={
                "num_questions": num_questions,
                "difficulty": "medium",
                "question_type": "multiple_choice",
                "model": settings.quiz_model,
            },
        )
        response.raise_for_status()
        return response.json()
