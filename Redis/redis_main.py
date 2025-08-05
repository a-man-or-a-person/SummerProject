import os

from dotenv import load_dotenv

import redis.asyncio
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId

load_dotenv()


async def redis_conn():
    # Connect to local Redis (default settings)
    r = redis.asyncio.Redis(
        host="localhost",
        port=6379,
        db=0,  # Database index (0-15)
        password=None,  # If your Redis requires authentication
    )
    return r


async def redis_insert_link(url: LongUrl, short_id: int):
    r = await redis_conn()
    await r.setex(f"{short_id}", int(os.getenv("EXP_TIME")), f"{str(url.url)}")
    await r.close()


async def redis_get_link(short_id: ShortLinkId):
    r = await redis_conn()
    link_id = short_id.id
    link_exists = await r.exists(f"{link_id}")
    if link_exists:
        long_link = await r.get(f"{link_id}")
        long_link_class = LongUrl(url=long_link)
        await r.close()
        return long_link_class
    else:
        await r.close()
        return None
