from sqlalchemy import select

from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId
from Redis.redis_main import redis_get_link, redis_insert_link
from test_db.database import Base, async_engine, async_session_factory
from test_db.models import LinkStorage


async def drop_tables():
    async with async_engine.connect() as conn:
        async_engine.echo = True
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


async def insert_link(long_link_u=LongUrl) -> int:
    async with async_session_factory() as session:
        link = LinkStorage(long_link=str(long_link_u.url))
        session.add(link)
        await session.flush()
        gen_link_id = link.id
        await session.commit()
        return gen_link_id


async def get_long_link_db(link_id=ShortLinkId) -> LongUrl:
    async with async_session_factory() as session:
        query = select(LinkStorage.long_link).where(LinkStorage.id.is_(link_id.id))
        long_link = await session.execute(query)
        long_link = long_link.scalar_one()
        long_link = LongUrl(url=long_link)
        return long_link
