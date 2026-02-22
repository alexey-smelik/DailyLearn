"""Scheduler job: find due learning cards and dispatch notifications."""

import logging
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.tg_tool import CardNotification, send_card_notification
from app.database import async_session_factory
from app.models.learning_card import LearningCard
from app.models.newsletter import Newsletter
from app.scheduler.service import is_due

logger = logging.getLogger(__name__)


async def _get_due_cards(session: AsyncSession) -> list[tuple[LearningCard, datetime, int]]:
    """Return (card, last_send_date, newsletter_count) for every due card."""
    # Cards that have at least one newsletter and have tg_chat_id configured
    subq = (
        select(
            Newsletter.learning_card_id,
            func.max(Newsletter.send_date).label("last_send"),
            func.count(Newsletter.id).label("total"),
        )
        .group_by(Newsletter.learning_card_id)
        .subquery()
    )

    result = await session.execute(
        select(LearningCard, subq.c.last_send, subq.c.total)
        .join(subq, LearningCard.id == subq.c.learning_card_id)
        .where(LearningCard.tg_chat_id.is_not(None))
        .where(LearningCard.is_active.is_(True))
    )

    due = []
    for card, last_send, total in result.all():
        last_send_aware = last_send.replace(tzinfo=timezone.utc) if last_send.tzinfo is None else last_send
        if is_due(last_send_aware, total, card.schedule):
            due.append((card, last_send_aware, total))
    return due


async def _record_newsletter(session: AsyncSession, card: LearningCard) -> None:
    now = datetime.now(tz=timezone.utc)
    newsletter = Newsletter(
        user_id=card.user_id,
        learning_card_id=card.id,
        send_date=now,
    )
    session.add(newsletter)
    await session.flush()


async def dispatch_due_cards() -> None:
    """Entry point called by APScheduler."""
    logger.info("Checking for due learning cards...")
    async with async_session_factory() as session:
        async with session.begin():
            due_cards = await _get_due_cards(session)
            logger.info("Found %d due card(s)", len(due_cards))

            for card, _last_send, _count in due_cards:
                notification = CardNotification(
                    tg_chat_id=card.tg_chat_id,  # type: ignore[arg-type]
                    tg_topic_id=card.tg_topic_id,
                    card_id=card.id,
                    card_name=card.name,
                    source_url=card.source_url,
                    schedule=card.schedule,
                    message_template=card.message_template,
                )
                try:
                    await send_card_notification(notification)
                    await _record_newsletter(session, card)
                    logger.info("Sent notification for card '%s'", card.name)
                except Exception:
                    logger.exception("Failed to send notification for card '%s'", card.name)
                    # Roll back only this card; continue with others via savepoint
                    await session.rollback()
                    async with session.begin():
                        pass  # reopen transaction for remaining cards
