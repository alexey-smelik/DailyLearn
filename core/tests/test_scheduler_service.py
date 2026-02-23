from datetime import datetime, timedelta, timezone

import pytest

from app.scheduler.service import DEFAULT_INTERVALS, is_due, next_review_date, parse_schedule


class TestParseSchedule:
    def test_parse_days(self) -> None:
        result = parse_schedule("1d → 3d → 7d → 14d → 30d → 90d")
        assert result == [
            timedelta(days=1), timedelta(days=3), timedelta(days=7),
            timedelta(days=14), timedelta(days=30), timedelta(days=90),
        ]

    def test_parse_minutes(self) -> None:
        assert parse_schedule("1m → 2m → 3m") == [
            timedelta(minutes=1), timedelta(minutes=2), timedelta(minutes=3),
        ]

    def test_parse_hours(self) -> None:
        assert parse_schedule("2h → 12h → 24h") == [
            timedelta(hours=2), timedelta(hours=12), timedelta(hours=24),
        ]

    def test_parse_mixed_units(self) -> None:
        assert parse_schedule("5m → 1h → 3d") == [
            timedelta(minutes=5), timedelta(hours=1), timedelta(days=3),
        ]

    def test_parse_none_returns_default(self) -> None:
        assert parse_schedule(None) == DEFAULT_INTERVALS

    def test_parse_empty_string_returns_default(self) -> None:
        assert parse_schedule("") == DEFAULT_INTERVALS

    def test_parse_unparsable_returns_default(self) -> None:
        assert parse_schedule("no intervals here") == DEFAULT_INTERVALS

    def test_parse_case_insensitive(self) -> None:
        assert parse_schedule("1D → 3D") == [timedelta(days=1), timedelta(days=3)]


class TestNextReviewDate:
    def _now(self) -> datetime:
        return datetime(2025, 1, 10, 12, 0, tzinfo=timezone.utc)

    @pytest.mark.parametrize(
        "newsletter_count,expected",
        [
            (1, timedelta(days=1)),
            (2, timedelta(days=3)),
            (3, timedelta(days=7)),
            (4, timedelta(days=14)),
            (5, timedelta(days=30)),
            (6, timedelta(days=90)),
            (7, timedelta(days=90)),   # beyond list → repeat last
            (99, timedelta(days=90)),
        ],
    )
    def test_standard_intervals(self, newsletter_count: int, expected: timedelta) -> None:
        base = self._now()
        assert next_review_date(base, newsletter_count, None) == base + expected

    def test_custom_days_schedule(self) -> None:
        base = self._now()
        assert next_review_date(base, 1, "2d → 10d → 30d") == base + timedelta(days=2)

    def test_custom_minutes_schedule(self) -> None:
        base = self._now()
        assert next_review_date(base, 1, "1m → 2m → 3m") == base + timedelta(minutes=1)

    def test_custom_mixed_schedule(self) -> None:
        base = self._now()
        assert next_review_date(base, 2, "5m → 1h → 3d") == base + timedelta(hours=1)


class TestIsDue:
    def test_is_due_when_overdue(self) -> None:
        old_send = datetime.now(tz=timezone.utc) - timedelta(days=10)
        assert is_due(old_send, 1, "1d → 3d") is True

    def test_not_due_when_future(self) -> None:
        recent_send = datetime.now(tz=timezone.utc) - timedelta(hours=1)
        assert is_due(recent_send, 1, "1d → 3d") is False

    def test_due_exactly_on_time(self) -> None:
        send = datetime.now(tz=timezone.utc) - timedelta(days=1)
        assert is_due(send, 1, "1d") is True

    def test_due_with_minutes_schedule(self) -> None:
        send = datetime.now(tz=timezone.utc) - timedelta(minutes=2)
        assert is_due(send, 1, "1m → 2m → 3m") is True

    def test_not_due_with_minutes_schedule(self) -> None:
        send = datetime.now(tz=timezone.utc) - timedelta(seconds=30)
        assert is_due(send, 1, "1m → 2m → 3m") is False
