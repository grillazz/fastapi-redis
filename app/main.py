from aioredis import Redis, create_redis_pool
from fastapi import Depends, FastAPI
from rdkit.Chem import MolFromSmiles, RDKFingerprint
from rdkit.DataStructs import FingerprintSimilarity

from app import config
from app.schemas import CompoundsListSchema

global_settings = config.Settings()


app = FastAPI()


async def init_redis_pool() -> Redis:
    redis = await create_redis_pool(
        global_settings.redis_url,
        password=global_settings.redis_password,
        encoding="utf-8",
        db=global_settings.redis_db,
    )
    return redis


@app.on_event("startup")
async def starup_event():
    app.state.redis = await init_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.get("/health-check")
async def health_check(settings: config.Settings = Depends(config.get_settings)):
    try:
        await app.state.redis.set(str(settings.redis_url), settings.up)
        value = await app.state.redis.get(str(settings.redis_url))
    except:  # noqa: E722
        value = settings.down
    return {settings.web_server: settings.up, str(settings.redis_url): value}


@app.post("/add-smiles")
async def add_canonical_smiles_to_hash(payload: CompoundsListSchema, redis_hash: str):

    mols = {}
    # filter SMILES from compounds and add to molecule dict
    for compound in payload.PC_Compounds:
        mols.update(
            {x.value.sval: "SMILES" for x in compound.props if x.urn.label == "SMILES" and x.urn.name == "Canonical"}
        )

    # save molecules to redis hash
    for k, v in mols.items():
        await app.state.redis.hset(redis_hash, k, v)

    # TODO: test hset with k:v list as one insert
    hash_len = await app.state.redis.hlen(redis_hash)
    return {
        "number_of_inserted_keys": hash_len,
        "hash_name": redis_hash
    }


@app.get("/compare-smiles")
async def get_smiles_and_compare(compound: str, redis_hash: str):
    mol = RDKFingerprint(MolFromSmiles(compound))

    mol_hash = await app.state.redis.hgetall(redis_hash)

    similarity = {
            smile: FingerprintSimilarity(RDKFingerprint(MolFromSmiles(smile)), mol)
            for smile, value in mol_hash.items()
    }

    return {
        "number_of_smiles_to_compare": len(similarity),
        "similarity": dict(
            sorted(similarity.items(), key=lambda item: item[1], reverse=True)
        ),
    }
