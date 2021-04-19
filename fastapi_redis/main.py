from fastapi import FastAPI, Depends
from aioredis import create_redis_pool, Redis


from fastapi_redis import config

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


# 1. get list of SMILES
# 2. loop over it d2 = {k: f(v) for k, v in d1.items()} like fps = [Chem.RDKFingerprint(x) for x in ms]
# to build {k:v} for redis HSET
# 3. insert HSET as async call to redis
