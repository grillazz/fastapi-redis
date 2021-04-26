from fastapi import FastAPI, Depends, Request
from aioredis import create_redis_pool, Redis
from app.schemas import CompoundsListSchema

from app import config

from rdkit.Chem import RDKFingerprint, MolFromSmiles
from rdkit.Chem.Fingerprints.FingerprintMols import FingerprintMol, GetRDKFingerprint
from rdkit.DataStructs import FingerprintSimilarity

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
async def add_smiles(payload: CompoundsListSchema):

    mols = {}
    for compound in payload.PC_Compounds:
        mols.update({x.value.sval: str(RDKFingerprint(MolFromSmiles(x.value.sval)).ToBinary()) for x in compound.props})

    for k, v in mols.items():
        await app.state.redis.hset("mols:figers", k,v)

    return await app.state.redis.hgetall("mols:figers")
# 1. get list of SMILES
# 2. loop over it d2 = {k: f(v) for k, v in d1.items()} like fps = [Chem.RDKFingerprint(x) for x in ms]
# to build {k:v} for redis HSET
# 3. insert HSET as async call to redis
