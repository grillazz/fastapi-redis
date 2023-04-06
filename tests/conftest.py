import json
import pathlib

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.redis import init_redis_pool
from app.service import MoleculesRepository


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ]
)
def anyio_backend(request):
    return request.param


@pytest.fixture(autouse=True)
def get_payload(request):
    path = pathlib.Path(request.node.fspath.strpath)
    file = path.with_name("PubChem_compound_text_covid-19_records.json")
    with file.open() as compounds:
        return json.load(compounds)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.state.redis = await init_redis_pool()
        app.state.mols_repo = MoleculesRepository(app.state.redis)
        yield ac
        await app.state.redis.close()
