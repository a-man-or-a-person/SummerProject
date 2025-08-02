from test_db.database import Base, async_session_factory, async_engine
from test_db.models import LinkStorage
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId
from sqlalchemy import select


async def drop_tables():
    async with async_engine.connect() as conn:
        async_engine.echo = True
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


async def insert_link(long_link_u=LongUrl) -> int:
    async with async_session_factory() as session:
        print('LINK:', long_link_u.url)
        link = LinkStorage(long_link=str(long_link_u.url))
        session.add(link)
        await session.flush()
        gen_link_id = link.id
        await session.commit()
        return gen_link_id


async def get_long_link(link_id=ShortLinkId):
    async with async_session_factory() as session:
        query = select(LinkStorage.long_link).where(LinkStorage.id.is_(link_id.id))
        long_link = await session.execute(query)
        long_link = long_link.scalar_one()
        long_link = LongUrl(url=long_link)
        return long_link
