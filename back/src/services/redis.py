import redis.asyncio as redis
from src.config import config
from redis.asyncio.client import Redis


class RedisHelper():
    _instance = None
    _client = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(RedisHelper, cls).__new__(cls)
            pool = redis.ConnectionPool.from_url(config.redis.get_url)
            cls._client = redis.Redis.from_pool(pool)
        return cls._instance
        
    async def get_redis(self) -> Redis:
        if not isinstance(RedisHelper._client, Redis):
            raise
        return RedisHelper._client


redis_helper = RedisHelper()
