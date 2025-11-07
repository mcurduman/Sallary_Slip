import redis.asyncio as aioredis
from idemptx.backend.redis import AsyncRedisBackend

redis_client = aioredis.Redis(host='redis', port=6379, db=0)
async_redis_backend = AsyncRedisBackend(redis_client)