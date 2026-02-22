import pytest
from httpx import AsyncClient


@pytest.fixture
async def user_id(client: AsyncClient) -> int:
    resp = await client.post("/api/v1/users", json={"login": "card_owner"})
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.fixture
async def created_card(client: AsyncClient, user_id: int) -> dict:
    resp = await client.post(
        "/api/v1/learning-cards",
        json={"name": "FastAPI basics", "source_url": "https://fastapi.tiangolo.com", "user_id": user_id},
    )
    assert resp.status_code == 201
    return resp.json()


async def test_create_learning_card_valid_data_returns_201(
    client: AsyncClient, user_id: int
) -> None:
    resp = await client.post(
        "/api/v1/learning-cards",
        json={"name": "SQLAlchemy", "user_id": user_id},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "SQLAlchemy"
    assert data["source_url"] is None
    assert data["user_id"] == user_id


async def test_get_learning_card_existing_returns_200(
    client: AsyncClient, created_card: dict
) -> None:
    resp = await client.get(f"/api/v1/learning-cards/{created_card['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == created_card["name"]


async def test_get_learning_card_nonexistent_returns_404(client: AsyncClient) -> None:
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    resp = await client.get(f"/api/v1/learning-cards/{fake_uuid}")
    assert resp.status_code == 404


async def test_list_learning_cards_returns_all(
    client: AsyncClient, created_card: dict
) -> None:
    resp = await client.get("/api/v1/learning-cards")
    assert resp.status_code == 200
    ids = [c["id"] for c in resp.json()]
    assert created_card["id"] in ids


async def test_update_learning_card_name_returns_updated(
    client: AsyncClient, created_card: dict
) -> None:
    resp = await client.patch(
        f"/api/v1/learning-cards/{created_card['id']}",
        json={"name": "FastAPI advanced"},
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "FastAPI advanced"


async def test_delete_learning_card_existing_returns_204(
    client: AsyncClient, created_card: dict
) -> None:
    resp = await client.delete(f"/api/v1/learning-cards/{created_card['id']}")
    assert resp.status_code == 204

    resp = await client.get(f"/api/v1/learning-cards/{created_card['id']}")
    assert resp.status_code == 404
