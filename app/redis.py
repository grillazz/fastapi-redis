import redis.asyncio as redis

from app import config

global_settings = config.Settings()


async def init_redis_pool() -> redis.Redis:
    redis_c = await redis.from_url(
        global_settings.redis_url,
        encoding="utf-8",
        db=global_settings.redis_db,
        decode_responses=True,
    )
    return redis_c
