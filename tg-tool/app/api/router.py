import logging

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import APIRouter, Request

from app.api.schemas import ConspectRequestBody, SendRequest, SendResponse
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
    control_row = []
    if body.show_pause_button:
        control_row.append(
            InlineKeyboardButton(text="⏸ Pause", callback_data=f"toggle:{body.card_id}")
        )
    if body.show_skip_button:
        control_row.append(
            InlineKeyboardButton(text="⏭ Skip", callback_data=f"skip:{body.card_id}")
        )

    inline_rows = []
    if control_row:
        inline_rows.append(control_row)
    if body.show_quiz_button and body.has_conspect:
        inline_rows.append([
            InlineKeyboardButton(text="🧠 Take a quiz", callback_data=f"quiz:{body.card_id}")
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_rows) if inline_rows else None
    await bot.send_message(
        chat_id=body.tg_chat_id,
        text=text,
        parse_mode="HTML",
        message_thread_id=body.tg_topic_id or None,
        reply_markup=keyboard,
    )
    logger.info("Sent card '%s' to chat %s", body.card_name, body.tg_chat_id)
    return SendResponse(ok=True)


@router.post("/send-conspect-request", response_model=SendResponse)
async def send_conspect_request(request: Request, body: ConspectRequestBody) -> SendResponse:
    """Send a conspect request message with a 'Write notes' inline button."""
    bot: Bot = request.app.state.bot
    duration_str = f" (study time: <b>{body.time_to_educate}</b>)" if body.time_to_educate else ""
    text = (
        f"📝 <b>Time to write your study notes!</b>{duration_str}\n\n"
        f"Card: <b>{body.card_name}</b>\n\n"
        f"Click the button below and send your conspect in the next message."
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="✍️ Write notes",
                callback_data=f"write_conspect:{body.card_id}",
            )
        ]]
    )
    await bot.send_message(
        chat_id=body.tg_chat_id,
        text=text,
        parse_mode="HTML",
        message_thread_id=body.tg_topic_id or None,
        reply_markup=keyboard,
    )
    logger.info("Sent conspect request for card '%s' to chat %s", body.card_name, body.tg_chat_id)
    return SendResponse(ok=True)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
