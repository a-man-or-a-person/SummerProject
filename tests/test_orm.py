# tests/test_orm.py
import pytest
from DB.orm import insert_link, get_long_link_db
from DB.models import LinkStorage
from DB.database import Base, async_engine, async_session_factory
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId
from sqlalchemy import select


@pytest.mark.asyncio
async def test_insert_and_retrieve_link():
    # Тестовая сессия
    async with async_session_factory() as session:
        # Очистка таблицы перед тестом
        await session.execute(LinkStorage.__table__.delete())
        await session.commit()

        # Тестовые данные
        long_url = "https://test.com"
        short_id = "test123"

        # Вставка
        await insert_link(LongUrl(url=long_url), short_id)

        # Получение
        result = await get_long_link_db(ShortLinkId(id=short_id))
        assert result.url == long_url