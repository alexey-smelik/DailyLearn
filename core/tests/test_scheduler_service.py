from datetime import datetime, timedelta, timezone

import pytest

from app.scheduler.service import DEFAULT_INTERVALS, is_due, next_review_date, parse_schedule


class TestParseSchedule:
    def test_parse_valid_schedule(self) -> None:
        result = parse_schedule("1d → 3d → 7d → 14d → 30d → 90d")
        assert result == [1, 3, 7, 14, 30, 90]

    def test_parse_custom_schedule(self) -> None:
        result = parse_schedule("2d → 5d → 10d")
        assert result == [2, 5, 10]

    def test_parse_none_returns_default(self) -> None:
        assert parse_schedule(None) == DEFAULT_INTERVALS

    def test_parse_empty_string_returns_default(self) -> None:
        assert parse_schedule("") == DEFAULT_INTERVALS

    def test_parse_unparsable_returns_default(self) -> None:
        assert parse_schedule("no intervals here") == DEFAULT_INTERVALS

    def test_parse_case_insensitive(self) -> None:
        assert parse_schedule("1D → 3D") == [1, 3]


class TestNextReviewDate:
    def _now(self) -> datetime:
        return datetime(2025, 1, 10, 12, 0, tzinfo=timezone.utc)

    @pytest.mark.parametrize(
        "newsletter_count,expected_days",
        [
            (1, 1),   # first interval after initial tg-tool send
            (2, 3),
            (3, 7),
            (4, 14),
            (5, 30),
            (6, 90),
            (7, 90),  # beyond list → repeat last
            (99, 90),
        ],
    )
    def test_standard_intervals(self, newsletter_count: int, expected_days: int) -> None:
        base = self._now()
        result = next_review_date(base, newsletter_count, None)
        assert result == base + timedelta(days=expected_days)

    def test_custom_schedule(self) -> None:
        base = self._now()
        result = next_review_date(base, 1, "2d → 10d → 30d")
        assert result == base + timedelta(days=2)


class TestIsDue:
    def test_is_due_when_overdue(self) -> None:
        old_send = datetime.now(tz=timezone.utc) - timedelta(days=10)
        assert is_due(old_send, 1, "1d → 3d") is True

    def test_not_due_when_future(self) -> None:
        recent_send = datetime.now(tz=timezone.utc) - timedelta(hours=1)
        assert is_due(recent_send, 1, "1d → 3d") is False

    def test_due_exactly_on_time(self) -> None:
        # Sent exactly 1 day ago → due now
        send = datetime.now(tz=timezone.utc) - timedelta(days=1)
        assert is_due(send, 1, "1d") is True
