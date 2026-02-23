import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.states import ConspectStates
from app.clients.web_api import generate_quiz, save_conspect, skip_card, toggle_card

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


@router.callback_query(F.data.startswith("skip:"))
async def callback_skip_card(callback: CallbackQuery) -> None:
    card_id = callback.data.split(":", 1)[1]  # type: ignore[union-attr]
    try:
        await skip_card(card_id)
        await callback.answer("⏭ Iteration skipped", show_alert=False)
    except Exception:
        logger.exception("Failed to skip card %s", card_id)
        await callback.answer("❌ Failed to skip. Try again.", show_alert=True)


@router.callback_query(F.data.startswith("write_conspect:"))
async def callback_write_conspect(callback: CallbackQuery, state: FSMContext) -> None:
    card_id = callback.data.split(":", 1)[1]  # type: ignore[union-attr]
    topic_id = callback.message.message_thread_id if callback.message else None  # type: ignore[union-attr]
    await state.set_state(ConspectStates.waiting)
    await state.update_data(card_id=card_id, topic_id=topic_id)
    await callback.answer()
    await callback.message.reply("✍️ Please write your study notes for this card:")  # type: ignore[union-attr]


@router.callback_query(F.data.startswith("quiz:"))
async def callback_quiz(callback: CallbackQuery) -> None:
    card_id = callback.data.split(":", 1)[1]  # type: ignore[union-attr]
    await callback.answer()
    status_msg = await callback.message.reply("🧠 Generating your quiz, please wait…")  # type: ignore[union-attr]
    try:
        quiz = await generate_quiz(card_id)
        text = _format_quiz(quiz)
        await status_msg.delete()
        await callback.message.reply(text, parse_mode="HTML")  # type: ignore[union-attr]
    except Exception:
        logger.exception("Failed to generate quiz for card %s", card_id)
        await status_msg.delete()
        await callback.message.reply("❌ Could not generate quiz. Try again later.")  # type: ignore[union-attr]


def _format_quiz(quiz: dict) -> str:
    lines: list[str] = [f"🧠 <b>Quiz</b> · {quiz.get('difficulty', '')} · {len(quiz.get('questions', []))} questions\n"]
    for idx, q in enumerate(quiz.get("questions", []), start=1):
        lines.append(f"<b>Q{idx}.</b> {q['question']}")
        if "options" in q:
            # multiple_choice
            for opt in q["options"]:
                lines.append(f"  {opt}")
            answer = q.get("correct_answer", "")
            explanation = q.get("explanation", "")
            lines.append(f"<tg-spoiler>✅ {answer}" + (f"\n💡 {explanation}" if explanation else "") + "</tg-spoiler>")
        else:
            # open
            sample = q.get("sample_answer", "")
            key_points = q.get("key_points", [])
            spoiler_text = f"📝 {sample}"
            if key_points:
                spoiler_text += "\n\nKey points:\n" + "\n".join(f"• {p}" for p in key_points)
            lines.append(f"<tg-spoiler>{spoiler_text}</tg-spoiler>")
        lines.append("")
    return "\n".join(lines)


@router.message(StateFilter(ConspectStates.waiting))
async def receive_conspect(message: Message, state: FSMContext) -> None:
    text = message.text or ""
    if not text.strip():
        await message.reply("Please send text as your study notes.")
        return
    data = await state.get_data()
    card_id: str = data["card_id"]
    try:
        await save_conspect(card_id, text.strip())
        await state.clear()
        await message.reply("✅ Study notes saved!")
    except Exception:
        logger.exception("Failed to save conspect for card %s", card_id)
        await message.reply("❌ Failed to save. Please try again.")
