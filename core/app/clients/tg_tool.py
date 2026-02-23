"""HTTP client for the tg-tool service."""

import uuid
from dataclasses import dataclass

import httpx

from app.config import settings


@dataclass
class ConspectRequest:
    tg_chat_id: str
    tg_topic_id: int | None
    card_id: uuid.UUID
    card_name: str
    time_to_educate: str | None


@dataclass
class CardNotification:
    tg_chat_id: str
    tg_topic_id: int | None
    card_id: uuid.UUID
    card_name: str
    source_url: str | None
    schedule: str | None
    message_template: str | None
    show_pause_button: bool = True
    show_skip_button: bool = True
    show_quiz_button: bool = False
    has_conspect: bool = False


async def send_conspect_request(req: ConspectRequest) -> None:
    """POST conspect request to tg-tool /send-conspect-request endpoint."""
    payload = {
        "tg_chat_id": req.tg_chat_id,
        "tg_topic_id": req.tg_topic_id,
        "card_id": str(req.card_id),
        "card_name": req.card_name,
        "time_to_educate": req.time_to_educate,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(f"{settings.tg_tool_url}/send-conspect-request", json=payload)
        response.raise_for_status()


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
        "show_pause_button": notification.show_pause_button,
        "show_skip_button": notification.show_skip_button,
        "show_quiz_button": notification.show_quiz_button,
        "has_conspect": notification.has_conspect,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(f"{settings.tg_tool_url}/send", json=payload)
        response.raise_for_status()
