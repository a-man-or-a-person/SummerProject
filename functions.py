import hashlib
import base62
from fastapi import HTTPException
from redis.exceptions import RedisError
from test_db.orm import get_long_link_db, insert_link
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId, settings
from Redis.redis_main import redis_get_link, redis_insert_link

async def gen_short_id(url: LongUrl, length=settings.short_id_length) -> str:
    if not 1 <= length <= 32:
        raise ValueError('Identifier length must be between 1 and 32')
    value = int(hashlib.sha256(str(url.url).encode()).hexdigest(), 16)
    return base62.encode(value).zfill(43)[:length]

async def convert_long_link(long_link_u: LongUrl) -> str:
    short_id = await gen_short_id(long_link_u)
    await insert_link(long_link_u, short_id)
    try:
        await redis_insert_link(long_link_u, short_id)
    except RedisError:
        pass  # The durable write succeeded; a cache outage must not invalidate it.
    return short_id

async def get_long_link(short_id: ShortLinkId) -> LongUrl:
    try:
        cached = await redis_get_link(short_id)
        if cached:
            return cached
    except RedisError:
        pass
    stored = await get_long_link_db(short_id)
    if stored is None:
        raise HTTPException(status_code=404, detail='Unknown short link')
    return stored
