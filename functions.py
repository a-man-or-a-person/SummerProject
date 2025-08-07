import hashlib

import base62

from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId, settings
from Redis.redis_main import redis_get_link, redis_insert_link
from test_db.orm import get_long_link_db, insert_link


async def gen_short_id(url: LongUrl, length=settings.short_id_length) -> str:
    url_hash = hashlib.sha256(str(url.url).encode()).hexdigest()
    hash_int = int(url_hash[:8], 16)
    return base62.encode(hash_int)[:length]


async def convert_long_link(long_link_u: LongUrl) -> str:
    short_id = await gen_short_id(url=long_link_u)
    await insert_link(long_link_u, short_id)  # INSERTING LINK TO DB
    await redis_insert_link(long_link_u, short_id)  # INSERTING LINK TO REDIS
    return short_id


async def get_long_link(short_id: ShortLinkId):
    redis_link = await redis_get_link(short_id)
    if redis_link:
        if settings.test_mode:
            print("REDIS")
        return redis_link
    else:
        if settings.test_mode:
            print("DB")
        db_link = await get_long_link_db(short_id)
        return db_link
