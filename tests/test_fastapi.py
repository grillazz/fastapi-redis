import fakeredis.aioredis
import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def test_app():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        server = fakeredis.FakeServer()
        app.state.redis = await fakeredis.aioredis.create_redis_pool(server=server)
        yield ac


@pytest.mark.asyncio
async def test_root(test_app):
    response = await test_app.get("/health-check")
    assert response.status_code == status.HTTP_200_OK
