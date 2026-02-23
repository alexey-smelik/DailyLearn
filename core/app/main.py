"""Core scheduler service entry point."""

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config import settings
from app.scheduler.jobs import dispatch_conspect_requests, dispatch_due_cards

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        dispatch_due_cards,
        trigger=IntervalTrigger(minutes=settings.check_interval_minutes),
        id="dispatch_due_cards",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.add_job(
        dispatch_conspect_requests,
        trigger=IntervalTrigger(minutes=settings.check_interval_minutes),
        id="dispatch_conspect_requests",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.start()
    logger.info(
        "Scheduler started — checking every %d minute(s)",
        settings.check_interval_minutes,
    )

    # Run initial check immediately on startup
    await dispatch_due_cards()

    try:
        await asyncio.Event().wait()  # run forever
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
