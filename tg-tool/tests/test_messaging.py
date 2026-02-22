import pytest

from app.messaging import build_message


class TestBuildMessage:
    def test_default_template(self) -> None:
        result = build_message("React hooks", None, None)
        assert "React hooks" in result
        assert "<b>" in result

    def test_custom_template_legacy_syntax(self) -> None:
        result = build_message("React hooks", None, "Повтори: {card_name}")
        assert result == "Повтори: React hooks"

    def test_custom_template_new_syntax_name(self) -> None:
        result = build_message("Общая психология", None, "Повтори: {{name}}")
        assert result == "Повтори: Общая психология"

    def test_custom_template_source_url_var(self) -> None:
        result = build_message("X", "https://example.com", "Ссылка: {{source_url}}", card_id="abc")
        assert "https://example.com" in result
        # source link is still appended
        assert "Source" in result

    def test_custom_template_schedule_var(self) -> None:
        result = build_message("X", None, "Schedule: {{schedule}}", schedule="1d → 3d → 7d")
        assert "Schedule: 1d → 3d → 7d" in result

    def test_custom_template_id_var(self) -> None:
        result = build_message("X", None, "ID: {{id}}", card_id="uuid-123")
        assert "ID: uuid-123" in result

    def test_unknown_placeholder_kept(self) -> None:
        result = build_message("X", None, "Hello {{unknown}}")
        assert "{{unknown}}" in result

    def test_source_url_appended(self) -> None:
        result = build_message("React hooks", "https://react.dev", None)
        assert "https://react.dev" in result
        assert "Source" in result

    def test_custom_template_with_source(self) -> None:
        result = build_message("Hooks", "https://example.com", "Review: {{name}}")
        assert result.startswith("Review: Hooks")
        assert "https://example.com" in result

    @pytest.mark.parametrize("url", [None, ""])
    def test_no_link_when_no_url(self, url: str | None) -> None:
        result = build_message("X", url, None)
        assert "Source" not in result

    def test_empty_schedule_var_when_not_provided(self) -> None:
        result = build_message("X", None, "Sched: {{schedule}}")
        assert result == "Sched: "

    def test_multiple_vars_in_template(self) -> None:
        result = build_message(
            "Python async",
            "https://docs.python.org",
            "{{name}} — {{schedule}}",
            schedule="1d → 7d",
        )
        assert result.startswith("Python async — 1d → 7d")
