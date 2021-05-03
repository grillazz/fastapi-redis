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
