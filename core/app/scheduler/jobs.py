"""Scheduler job: find due learning cards and dispatch notifications."""

import logging
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.tg_tool import CardNotification, ConspectRequest, send_card_notification, send_conspect_request
from app.database import async_session_factory
from app.models import LearningCard, Newsletter  # noqa: F401 – import all models to register mappers
from app.scheduler.service import is_due, parse_duration

logger = logging.getLogger(__name__)


async def _get_due_cards(session: AsyncSession) -> list[tuple[LearningCard, datetime, int]]:
    """Return (card, last_send_date, newsletter_count) for every due card.

    Cards with no newsletters yet use add_date as the baseline so that the
    first notification is sent automatically after intervals[0] from creation.
    """
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
        .outerjoin(subq, LearningCard.id == subq.c.learning_card_id)
        .where(LearningCard.tg_chat_id.is_not(None))
        .where(LearningCard.is_active.is_(True))
    )

    due = []
    for card, last_send, total in result.all():
        if last_send is None:
            # Never sent — use card creation date as baseline, count = 0
            baseline = card.add_date
            newsletter_count = 0
        else:
            baseline = last_send
            newsletter_count = total
        baseline_aware = baseline.replace(tzinfo=timezone.utc) if baseline.tzinfo is None else baseline
        if is_due(baseline_aware, newsletter_count, card.schedule):
            due.append((card, baseline_aware, newsletter_count))
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
                    show_pause_button=card.show_pause_button,
                    show_skip_button=card.show_skip_button,
                    show_quiz_button=card.show_quiz_button,
                    has_conspect=bool(card.conspect and card.conspect.strip()),
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


async def dispatch_conspect_requests() -> None:
    """Find cards whose time_to_educate has elapsed and send conspect request messages."""
    logger.info("Checking for conspect requests...")
    async with async_session_factory() as session:
        async with session.begin():
            result = await session.execute(
                select(LearningCard)
                .where(LearningCard.is_active.is_(True))
                .where(LearningCard.time_to_educate.is_not(None))
                .where(LearningCard.conspect.is_(None))
                .where(LearningCard.conspect_requested.is_(False))
                .where(LearningCard.tg_chat_id.is_not(None))
            )
            cards = list(result.scalars().all())
            logger.info("Found %d card(s) eligible for conspect request", len(cards))

            now = datetime.now(tz=timezone.utc)
            for card in cards:
                delta = parse_duration(card.time_to_educate)
                if delta is None:
                    continue
                add_date_aware = (
                    card.add_date.replace(tzinfo=timezone.utc)
                    if card.add_date.tzinfo is None
                    else card.add_date
                )
                if now < add_date_aware + delta:
                    continue
                try:
                    await send_conspect_request(
                        ConspectRequest(
                            tg_chat_id=card.tg_chat_id,  # type: ignore[arg-type]
                            tg_topic_id=card.tg_topic_id,
                            card_id=card.id,
                            card_name=card.name,
                            time_to_educate=card.time_to_educate,
                        )
                    )
                    card.conspect_requested = True
                    logger.info("Sent conspect request for card '%s'", card.name)
                except Exception:
                    logger.exception("Failed to send conspect request for card '%s'", card.name)
