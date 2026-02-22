"""HTTP client for the web-api service."""

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
