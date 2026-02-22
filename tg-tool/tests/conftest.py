import os
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

# Must be set before app.config is imported (Settings() runs at module load)
os.environ.setdefault("BOT_TOKEN", "0:test_token")

from app.main import create_app  # noqa: E402


@pytest.fixture
def mock_bot() -> AsyncMock:
    bot = AsyncMock()
    bot.send_message = AsyncMock(return_value=None)
    return bot


@pytest.fixture
async def client(mock_bot: AsyncMock) -> AsyncClient:
    app = create_app(mock_bot)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
