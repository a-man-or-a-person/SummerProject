from fastapi import HTTPException, status
from sqlalchemy import select

from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId
from test_db.database import Base, async_engine, async_session_factory
from test_db.models import LinkStorage


async def drop_tables():
    async with async_engine.connect() as conn:
        async_engine.echo = True
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


async def insert_link(long_link_u: LongUrl, short_link_id: str) -> dict:
    try:
        async with async_session_factory() as session:
            link = LinkStorage(
                long_link=str(long_link_u.url), short_link_id=short_link_id
            )
            session.add(link)
            await session.commit()
        return {"OK": True}
    except Exception as e:
        return {"OK": False, "details": e}


async def get_long_link_db(link_id: ShortLinkId) -> LongUrl:
    async with async_session_factory() as session:
        query = select(LinkStorage.long_link).where(
            LinkStorage.short_link_id.is_(link_id.id)
        )
        long_link = await session.execute(query)
        long_link = long_link.scalar_one()
        long_link = LongUrl(url=long_link)
        return long_link
