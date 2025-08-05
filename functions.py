import os

from dotenv import load_dotenv

from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId
from Redis.redis_main import redis_get_link, redis_insert_link
from test_db.orm import get_long_link_db, insert_link

load_dotenv()


async def convert_long_link(long_link_u=LongUrl) -> int:
    short_id = await insert_link(
        long_link_u
    )  # INSERTING LINK TO DB AND GETTING SHORT ID
    await redis_insert_link(long_link_u, short_id)  # INSERTING LINK TO REDIS
    return short_id


async def get_long_link(short_id: ShortLinkId):
    redis_link = await redis_get_link(short_id)
    if redis_link:
        if os.getenv("TEST") == "True":
            print("REDIS")
        return redis_link
    else:
        if os.getenv("TEST") == "True":
            print("DB")
        db_link = await get_long_link_db(short_id)
        return db_link
