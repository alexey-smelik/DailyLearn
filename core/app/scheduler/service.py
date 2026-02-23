"""Business logic: schedule parsing and due-card detection."""

import re
from datetime import datetime, timedelta, timezone

DEFAULT_INTERVALS: list[timedelta] = [
    timedelta(days=1),
    timedelta(days=3),
    timedelta(days=7),
    timedelta(days=14),
    timedelta(days=30),
    timedelta(days=90),
]

# Matches: 10m  2h  3d  (case-insensitive)
_INTERVAL_RE = re.compile(r"(\d+)\s*(m|h|d)", re.IGNORECASE)
_UNIT_MAP = {"m": "minutes", "h": "hours", "d": "days"}


def parse_duration(value: str | None) -> timedelta | None:
    """Parse a single duration string like '30m', '2h', '1d' into a timedelta.

    Returns None if the value is absent or unparsable.
    """
    if not value:
        return None
    match = _INTERVAL_RE.search(value)
    if not match:
        return None
    amount, unit = match.groups()
    return timedelta(**{_UNIT_MAP[unit.lower()]: int(amount)})


def parse_schedule(schedule: str | None) -> list[timedelta]:
    """Return list of timedelta intervals from a schedule string.

    Supported units: m (minutes), h (hours), d (days).
    Examples: '1d → 3d → 7d', '5m → 30m → 2h', '10m → 1d → 7d'

    Falls back to DEFAULT_INTERVALS if the string is absent or unparsable.
    """
    if not schedule:
        return DEFAULT_INTERVALS
    intervals = [
        timedelta(**{_UNIT_MAP[unit.lower()]: int(value)})
        for value, unit in _INTERVAL_RE.findall(schedule)
    ]
    return intervals if intervals else DEFAULT_INTERVALS


def next_review_date(last_send: datetime, newsletter_count: int, schedule: str | None) -> datetime:
    """Calculate when the card should be reviewed next.

    newsletter_count is the total number of newsletters already sent for this card.
    """
    intervals = parse_schedule(schedule)
    idx = min(max(0, newsletter_count - 1), len(intervals) - 1)
    return last_send + intervals[idx]


def is_due(last_send: datetime, newsletter_count: int, schedule: str | None) -> bool:
    """Return True if the card is due for review right now."""
    return next_review_date(last_send, newsletter_count, schedule) <= datetime.now(tz=timezone.utc)
