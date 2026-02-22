import pytest
from httpx import AsyncClient


@pytest.fixture
async def user_and_card(client: AsyncClient) -> dict:
    user = await client.post("/api/v1/users", json={"login": "newsletter_owner"})
    assert user.status_code == 201
    user_id = user.json()["id"]

    card = await client.post(
        "/api/v1/learning-cards",
        json={"name": "Spaced Repetition", "user_id": user_id},
    )
    assert card.status_code == 201
    return {"user_id": user_id, "card_id": card.json()["id"]}


@pytest.fixture
async def created_newsletter(client: AsyncClient, user_and_card: dict) -> dict:
    resp = await client.post(
        "/api/v1/newsletters",
        json={
            "user_id": user_and_card["user_id"],
            "learning_card_id": user_and_card["card_id"],
            "message_template": "Time to review: {card}",
            "send_date": "2026-03-01T09:00:00Z",
            "tg_chat_id": "-1001234567890",
        },
    )
    assert resp.status_code == 201
    return resp.json()


async def test_create_newsletter_valid_data_returns_201(
    client: AsyncClient, user_and_card: dict
) -> None:
    resp = await client.post(
        "/api/v1/newsletters",
        json={
            "user_id": user_and_card["user_id"],
            "learning_card_id": user_and_card["card_id"],
            "message_template": "Study now!",
            "send_date": "2026-04-01T10:00:00Z",
            "tg_chat_id": "-100987654321",
            "tg_topic_id": 42,
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["message_template"] == "Study now!"
    assert data["tg_topic_id"] == 42
    assert data["add_date"] is not None


async def test_get_newsletter_existing_returns_200(
    client: AsyncClient, created_newsletter: dict
) -> None:
    resp = await client.get(f"/api/v1/newsletters/{created_newsletter['id']}")
    assert resp.status_code == 200
    assert resp.json()["message_template"] == created_newsletter["message_template"]


async def test_get_newsletter_nonexistent_returns_404(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/newsletters/99999")
    assert resp.status_code == 404


async def test_list_newsletters_returns_all(
    client: AsyncClient, created_newsletter: dict
) -> None:
    resp = await client.get("/api/v1/newsletters")
    assert resp.status_code == 200
    ids = [n["id"] for n in resp.json()]
    assert created_newsletter["id"] in ids


async def test_update_newsletter_template_returns_updated(
    client: AsyncClient, created_newsletter: dict
) -> None:
    resp = await client.patch(
        f"/api/v1/newsletters/{created_newsletter['id']}",
        json={"message_template": "Updated reminder text"},
    )
    assert resp.status_code == 200
    assert resp.json()["message_template"] == "Updated reminder text"


async def test_delete_newsletter_existing_returns_204(
    client: AsyncClient, created_newsletter: dict
) -> None:
    resp = await client.delete(f"/api/v1/newsletters/{created_newsletter['id']}")
    assert resp.status_code == 204

    resp = await client.get(f"/api/v1/newsletters/{created_newsletter['id']}")
    assert resp.status_code == 404
