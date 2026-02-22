"""HTTP client for the tg-tool service."""

import uuid
from dataclasses import dataclass

import httpx

from app.config import settings


@dataclass
class CardNotification:
    tg_chat_id: str
    tg_topic_id: int | None
    card_id: uuid.UUID
    card_name: str
    source_url: str | None
    schedule: str | None
    message_template: str | None


async def send_card_notification(notification: CardNotification) -> None:
    """POST card data to tg-tool /send endpoint."""
    payload = {
        "tg_chat_id": notification.tg_chat_id,
        "tg_topic_id": notification.tg_topic_id,
        "card_id": str(notification.card_id),
        "card_name": notification.card_name,
        "source_url": notification.source_url,
        "schedule": notification.schedule,
        "message_template": notification.message_template,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(f"{settings.tg_tool_url}/send", json=payload)
        response.raise_for_status()
