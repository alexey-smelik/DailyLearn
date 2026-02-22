from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient


class TestSendEndpoint:
    async def test_send_returns_ok(self, client: AsyncClient, mock_bot: AsyncMock) -> None:
        response = await client.post(
            "/send",
            json={
                "tg_chat_id": "-100123456789",
                "card_id": "550e8400-e29b-41d4-a716-446655440000",
                "card_name": "React hooks",
            },
        )
        assert response.status_code == 200
        assert response.json() == {"ok": True}
        mock_bot.send_message.assert_awaited_once()

    async def test_send_passes_chat_id(self, client: AsyncClient, mock_bot: AsyncMock) -> None:
        await client.post(
            "/send",
            json={
                "tg_chat_id": "-999",
                "card_id": "550e8400-e29b-41d4-a716-446655440000",
                "card_name": "Python async",
            },
        )
        call_kwargs = mock_bot.send_message.call_args.kwargs
        assert call_kwargs["chat_id"] == "-999"

    async def test_send_passes_topic_id(self, client: AsyncClient, mock_bot: AsyncMock) -> None:
        await client.post(
            "/send",
            json={
                "tg_chat_id": "-100",
                "tg_topic_id": 42,
                "card_id": "550e8400-e29b-41d4-a716-446655440000",
                "card_name": "Async",
            },
        )
        call_kwargs = mock_bot.send_message.call_args.kwargs
        assert call_kwargs["message_thread_id"] == 42

    async def test_send_missing_card_name_returns_422(self, client: AsyncClient) -> None:
        response = await client.post(
            "/send",
            json={"tg_chat_id": "-100", "card_id": "uuid"},
        )
        assert response.status_code == 422


class TestHealthEndpoint:
    async def test_health(self, client: AsyncClient) -> None:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
