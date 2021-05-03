import json
import pathlib

import fakeredis.aioredis
import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app
# decorate all tests with @pytest.mark.asyncio
from app.service import MoleculesRepository

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def get_payload(request):
    path = pathlib.Path(request.node.fspath.strpath)
    file = path.with_name("PubChem_compound_text_covid-19_records.json")
    with file.open() as compounds:
        return json.load(compounds)


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        server = fakeredis.FakeServer()
        app.state.redis = await fakeredis.aioredis.create_redis_pool(server=server)
        app.state.mols_repo = MoleculesRepository(app.state.redis)
        yield ac


async def test_set_and_compare(client, get_payload):
    redis_hash = "covid-19"
    response = await client.post(
        f"/api/smiles/add-to-hash/?redis_hash={redis_hash}", json=get_payload
    )
    assert response.status_code == status.HTTP_201_CREATED
