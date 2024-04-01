from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from common import settings_redis


async def init_fast_api_cache():
    redis = aioredis.from_url(url=settings_redis.url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
