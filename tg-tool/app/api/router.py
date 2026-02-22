import logging

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import APIRouter, Request

from app.api.schemas import SendRequest, SendResponse
from app.messaging import build_message

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/send", response_model=SendResponse)
async def send(request: Request, body: SendRequest) -> SendResponse:
    """Send a learning card reminder to Telegram with an inline toggle button."""
    bot: Bot = request.app.state.bot
    text = build_message(
        body.card_name,
        body.source_url,
        body.message_template,
        schedule=body.schedule,
        card_id=body.card_id,
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="⏸ Pause reminders",
                callback_data=f"toggle:{body.card_id}",
            )
        ]]
    )
    await bot.send_message(
        chat_id=body.tg_chat_id,
        text=text,
        parse_mode="HTML",
        message_thread_id=body.tg_topic_id,
        reply_markup=keyboard,
    )
    logger.info("Sent card '%s' to chat %s", body.card_name, body.tg_chat_id)
    return SendResponse(ok=True)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
