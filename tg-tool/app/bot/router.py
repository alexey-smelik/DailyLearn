import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from app.clients.web_api import toggle_card

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "👋 <b>Welcome to DailyLearn Bot!</b>\n\n"
        "I send you spaced repetition reminders for your learning cards "
        "based on the Ebbinghaus Forgetting Curve.\n\n"
        "To connect a card to this chat:\n"
        "1. Run /get_chat_id and copy the Chat ID\n"
        "2. Paste it into the card settings in the web UI",
        parse_mode="HTML",
    )


@router.message(Command("get_chat_id"))
async def cmd_get_chat_id(message: Message) -> None:
    lines = [f"<b>Chat ID:</b> <code>{message.chat.id}</code>"]
    if message.message_thread_id:
        lines.append(f"<b>Topic ID:</b> <code>{message.message_thread_id}</code>")
    await message.answer("\n".join(lines), parse_mode="HTML")


@router.callback_query(F.data.startswith("toggle:"))
async def callback_toggle_card(callback: CallbackQuery) -> None:
    card_id = callback.data.split(":", 1)[1]  # type: ignore[union-attr]
    try:
        card = await toggle_card(card_id)
        if card.get("is_active"):
            await callback.answer("▶️ Reminders resumed", show_alert=False)
        else:
            await callback.answer("⏸ Reminders paused", show_alert=False)
    except Exception:
        logger.exception("Failed to toggle card %s", card_id)
        await callback.answer("❌ Failed to toggle. Try again.", show_alert=True)
