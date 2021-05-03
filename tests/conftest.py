import json
import pathlib

import fakeredis.aioredis
import pytest
from httpx import AsyncClient

from app.main import app
from app.service import MoleculesRepository

# decorate all tests with @pytest.mark.asyncio
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
        app.state.redis.close()
        await app.state.redis.wait_closed()
