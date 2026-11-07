from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from test_db.database import Base, async_engine, async_session_factory
from test_db.models import LinkStorage
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def insert_link(long_link_u: LongUrl, short_link_id: str) -> None:
    async with async_session_factory() as session:
        try:
            session.add(LinkStorage(long_link=str(long_link_u.url), short_link_id=short_link_id))
            await session.commit()
        except IntegrityError:
            await session.rollback()
            existing = await session.get(LinkStorage, short_link_id)
            if existing is None or existing.long_link != str(long_link_u.url):
                raise HTTPException(status_code=409, detail='Short ID collision')

async def get_long_link_db(link_id: ShortLinkId) -> LongUrl | None:
    async with async_session_factory() as session:
        url = await session.scalar(select(LinkStorage.long_link).where(LinkStorage.short_link_id == link_id.id))
        return LongUrl(url=url) if url is not None else None
