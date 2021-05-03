from aioredis import Redis, create_redis_pool, create_sentinel

from app import config

global_settings = config.Settings()


async def init_redis_pool() -> Redis:
    if global_settings.use_redis_sentinel:
        sentinel = await create_sentinel(
            [(global_settings.redis_sentinel_url, global_settings.redis_sentinel_port)],
            db=global_settings.redis_db,
            password=global_settings.redis_password,
            encoding="utf-8",
        )
        redis = sentinel.master_for(global_settings.redis_sentinel_master_name)
    else:
        redis = await create_redis_pool(
            global_settings.redis_url,
            password=global_settings.redis_password,
            encoding="utf-8",
            db=global_settings.redis_db,
        )
    return redis
