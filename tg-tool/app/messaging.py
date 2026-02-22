"""Message text builder — pure function, easy to test."""

import re

DEFAULT_TEMPLATE = "📚 Time to review: <b>{{name}}</b>"

# All variables available in message templates.
# Documented here so the UI can list them.
TEMPLATE_VARS = ("name", "source_url", "schedule", "id")


def build_message(
    card_name: str,
    source_url: str | None,
    message_template: str | None,
    *,
    schedule: str | None = None,
    card_id: str | None = None,
) -> str:
    """Render the Telegram message text (HTML parse mode).

    Supported placeholder syntax:
      {{name}}        — card name
      {{source_url}}  — source URL (empty string if not set)
      {{schedule}}    — schedule string (empty string if not set)
      {{id}}          — card UUID

    Legacy ``{card_name}`` syntax is also accepted for backward compatibility.

    A source link is appended when ``source_url`` is present.
    """
    template = message_template if message_template else DEFAULT_TEMPLATE

    variables: dict[str, str] = {
        "name": card_name,
        "source_url": source_url or "",
        "schedule": schedule or "",
        "id": card_id or "",
        "card_name": card_name,  # legacy
    }

    def _replace(m: re.Match) -> str:  # type: ignore[type-arg]
        key = m.group(1)
        return variables.get(key, m.group(0))

    # New syntax: {{key}}
    text = re.sub(r"\{\{(\w+)\}\}", _replace, template)
    # Legacy syntax: {key}
    text = re.sub(r"\{(\w+)\}", _replace, text)

    if source_url:
        text += f'\n🔗 <a href="{source_url}">Source</a>'
    return text
