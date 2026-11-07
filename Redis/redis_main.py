from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId, settings
from redis.asyncio import ConnectionPool, Redis

redis_pool = ConnectionPool.from_url(settings.redis_url, socket_connect_timeout=1, socket_timeout=1)

async def redis_insert_link(url: LongUrl, short_id: str):
    async with Redis(connection_pool=redis_pool) as client:
        await client.setex(short_id, settings.exp_time, str(url.url))

async def redis_get_link(short_id: ShortLinkId) -> LongUrl | None:
    async with Redis(connection_pool=redis_pool) as client:
        value = await client.get(short_id.id)
        return LongUrl(url=value) if value is not None else None
