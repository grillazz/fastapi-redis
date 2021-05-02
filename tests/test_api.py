import time
import pytest
from httpx import AsyncClient
import fakeredis.aioredis
from fastapi import status

from tx_ws_api.main import app
from tx_ws_api.service.user_repository import UserRepository


@pytest.fixture
async def test_app():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        server = fakeredis.FakeServer()
        app.state.redis = await fakeredis.aioredis.create_redis_pool(server=server)
        app.state.user_repo = UserRepository(app.state.redis)
        yield ac


@pytest.mark.asyncio
async def test_root(test_app):
    response = await test_app.get("/health-check")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_users(test_app):
    response = await test_app.get("/get-users/dummy-business")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User presence doesn't exist."}


@pytest.mark.asyncio
async def test_get_users_expired(test_app):
    response = await test_app.get("/get-users-expired/dummy-business")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "data": {},
        "code": 200,
        "message": "User presence retrieved successfully",
    }


@pytest.mark.asyncio
async def test_set_user(test_app):
    payload = {"user_id": 123, "business_id": "Fantastic-Four"}
    response_post = await test_app.post("/set-user", json=payload)
    assert response_post.status_code == status.HTTP_201_CREATED
    response_get = await test_app.get("/get-users/Fantastic-Four")
    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json() == {
        "data": {"123": "1"},
        "code": 200,
        "message": "User presence retrieved successfully",
    }


@pytest.mark.asyncio
async def test_set_user_expired(test_app):
    payload = {"business_id": "Fantastic-Four", "user_id": 123, "expire": 3}
    response_post = await test_app.post("/set-user-expired", json=payload)
    assert response_post.status_code == status.HTTP_201_CREATED
    response_get = await test_app.get("/get-users-expired/Fantastic-Four")
    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json() == {
        "data": ["123"],
        "code": 200,
        "message": "User presence retrieved successfully",
    }
    time.sleep(4)
    response_get = await test_app.get("/get-users-expired/Fantastic-Four")
    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json() == {
        "data": {},
        "code": 200,
        "message": "User presence retrieved successfully",
    }
