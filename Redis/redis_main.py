from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId, settings
from redis.asyncio import ConnectionPool, Redis

redis_pool = ConnectionPool(
    host="localhost",
    port=6379,
    db=0,  # Database index (0-15)
    password=None,  # If your Redis requires authentication
)


async def redis_insert_link(url: LongUrl, short_id: str):
    async with Redis(connection_pool=redis_pool) as r:
        await r.setex(f"{short_id}", int(settings.exp_time), f"{str(url.url)}")


async def redis_get_link(short_id: ShortLinkId) -> LongUrl:
    async with Redis(connection_pool=redis_pool) as r:
        link_id = short_id.id
        link_exists = await r.exists(f"{link_id}")
        if link_exists:
            long_link = await r.get(f"{link_id}")
            long_link_class = LongUrl(url=long_link)

            return long_link_class
