import redis.asyncio as redis

from app.config import settings as global_settings


async def init_redis_pool() -> redis.Redis:
    redis_c = await redis.from_url(
        global_settings.redis_url.unicode_string(),
        encoding="utf-8",
        db=global_settings.redis_db,
        decode_responses=True,
    )
    return redis_c


# async def get_redis():
#     return await redis.from_url(
#         global_settings.redis_url.unicode_string(),
#         encoding="utf-8",
#         decode_responses=True,
#     )