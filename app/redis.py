from aioredis import Redis, from_url

from app import config

global_settings = config.Settings()


async def init_redis_pool() -> Redis:
    redis = await from_url(
        global_settings.redis_url,
        encoding="utf-8",
        db=global_settings.redis_db,
        decode_responses=True,
    )
    return redis
