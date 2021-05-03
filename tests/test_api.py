import pytest
from fastapi import status

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


async def test_set_and_compare(client, get_payload):
    redis_hash = "covid-19"
    response = await client.post(
        f"/api/smiles/add-to-hash/?redis_hash={redis_hash}", json=get_payload
    )
    assert response.status_code == status.HTTP_201_CREATED


async def test_api(client):
    response = await client.get("/health-check")
    assert response.status_code == status.HTTP_200_OK
