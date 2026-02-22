import pytest
from httpx import AsyncClient


@pytest.fixture
async def created_user(client: AsyncClient) -> dict:
    resp = await client.post("/api/v1/users", json={"login": "alice"})
    assert resp.status_code == 201
    return resp.json()


async def test_create_user_valid_data_returns_201(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/users", json={"login": "bob"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["login"] == "bob"
    assert data["id"] is not None
    assert data["last_visit"] is None


async def test_get_user_existing_id_returns_200(client: AsyncClient, created_user: dict) -> None:
    resp = await client.get(f"/api/v1/users/{created_user['id']}")
    assert resp.status_code == 200
    assert resp.json()["login"] == created_user["login"]


async def test_get_user_nonexistent_id_returns_404(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/users/99999")
    assert resp.status_code == 404


async def test_list_users_returns_all(client: AsyncClient, created_user: dict) -> None:
    resp = await client.get("/api/v1/users")
    assert resp.status_code == 200
    ids = [u["id"] for u in resp.json()]
    assert created_user["id"] in ids


async def test_update_user_login_returns_updated(client: AsyncClient, created_user: dict) -> None:
    resp = await client.patch(
        f"/api/v1/users/{created_user['id']}",
        json={"login": "alice_updated"},
    )
    assert resp.status_code == 200
    assert resp.json()["login"] == "alice_updated"


async def test_delete_user_existing_returns_204(client: AsyncClient, created_user: dict) -> None:
    resp = await client.delete(f"/api/v1/users/{created_user['id']}")
    assert resp.status_code == 204

    resp = await client.get(f"/api/v1/users/{created_user['id']}")
    assert resp.status_code == 404
