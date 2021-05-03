from aioredis import Redis


class MoleculesRepository:
    """Stores/Retrieves chem molecules from Redis Hash"""

    def __init__(self, redis: Redis):
        self._redis = redis

    async def set_multiple(self, key: str, smiles: dict):
        """Set multiple hash fields to multiple values.
        dict can be passed as first positional argument:

        """
        return await self._redis.hmset_dict(key, smiles)

    async def len(self, key: str):
        """Get the number of fields in a hash."""
        return await self._redis.hlen(key)

    # async def add(self, business_id: str, user_id: str, expire: int = 60):
    #     """Add a new user for business into the database
    #     with expiration time (TTL) in seconds. Same method is used for renewing
    #     user TTL in the database. User is automatically removed if TTL expires"""
    #     return await self._redis.setex(business_id + ":" + user_id, expire, user_id)
    #
    # async def get_all(self, business_id: str):
    #     """Get all users for a given business which TTL has not yet expired"""
    #     user_keys = await self._redis.keys(pattern=business_id + ":*")
    #     if user_keys:
    #         user_list = await self._redis.mget(*user_keys)
    #         return user_list
    #     return {}
    #
    # async def add_permanent(self, business_id: str, user_id: int):
    #     """Add a new permanent user for business into to the database.
    #     This method if used for testing purposes only"""
    #     return await self._redis.hset(business_id, user_id, 1)
    #
    # async def get_all_permanent(self, business_id: str):
    #     """Get all permanent users for given business.
    #     This method if used for testing purposes only"""
    #     return await self._redis.hgetall(business_id)
