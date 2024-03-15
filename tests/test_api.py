import pytest
from fastapi import status

from app import config

pytestmark = pytest.mark.anyio

global_settings = config.Settings()


@pytest.mark.parametrize(
    "response, status_code",
    (
        (
            {"number_of_inserted_keys": 5, "hash_name": global_settings.redis_hash},
            status.HTTP_201_CREATED,
        ),
    ),
)
async def test_set_fields_on_hash(
    client, get_payload, response: dict, status_code: int
):
    post_response = await client.post(
        f"/smiles/add-to-hash?redis_hash={global_settings.redis_hash}",
        json=get_payload,
    )
    assert post_response.status_code == status_code
    assert response == post_response.json()


@pytest.mark.parametrize(
    "response, status_code",
    (
        (
            {
                "number_of_smiles_to_compare": 5,
                "similarity": {
                    "C(C(C(=O)O)N)C(=O)N": 1.0,
                    "C([C@@H](C(=O)O)N)C(=O)N": 1.0,
                    "CCN(CC)CCCC(C)NC1=C2C=CC(=CC2=NC=C1)Cl": 0.07357859531772576,
                    "CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4": 0.059782608695652176,
                    "CCC(CC)COC(=O)[C@H](C)N[P@](=O)(OC[C@@H]1[C@H]([C@H]([C@](O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4": 0.059782608695652176,
                },
            },
            status.HTTP_200_OK,
        ),
    ),
)
async def test_compare_to_hash(client, get_payload, response: dict, status_code: int):
    compound = "C([C@@H](C(=O)O)N)C(=O)N"
    await client.post(
        f"/smiles/add-to-hash?redis_hash={global_settings.redis_hash}",
        json=get_payload,
    )

    get_response = await client.get(
        f"/smiles/compare-to-hash?redis_hash={global_settings.redis_hash}&compound={compound}"
    )
    assert get_response.status_code == status_code
    assert response == get_response.json()


async def test_api(client):
    response = await client.get("/health-check")
    assert response.status_code == status.HTTP_200_OK
