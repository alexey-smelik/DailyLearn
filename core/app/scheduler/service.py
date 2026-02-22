"""Business logic: schedule parsing and due-card detection."""

import re
from datetime import datetime, timedelta, timezone

DEFAULT_INTERVALS: list[int] = [1, 3, 7, 14, 30, 90]

_INTERVAL_RE = re.compile(r"(\d+)\s*d", re.IGNORECASE)


def parse_schedule(schedule: str | None) -> list[int]:
    """Return list of day-intervals from a schedule string like '1d → 3d → 7d'.

    Falls back to DEFAULT_INTERVALS if the string is absent or unparsable.
    """
    if not schedule:
        return DEFAULT_INTERVALS
    intervals = [int(m) for m in _INTERVAL_RE.findall(schedule)]
    return intervals if intervals else DEFAULT_INTERVALS


def next_review_date(last_send: datetime, newsletter_count: int, schedule: str | None) -> datetime:
    """Calculate when the card should be reviewed next.

    newsletter_count is the total number of newsletters already sent for this card.
    The index into the intervals list equals newsletter_count (0-based).
    """
    intervals = parse_schedule(schedule)
    idx = min(max(0, newsletter_count - 1), len(intervals) - 1)
    return last_send + timedelta(days=intervals[idx])


def is_due(last_send: datetime, newsletter_count: int, schedule: str | None) -> bool:
    """Return True if the card is due for review right now."""
    return next_review_date(last_send, newsletter_count, schedule) <= datetime.now(tz=timezone.utc)
