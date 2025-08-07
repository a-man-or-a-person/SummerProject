# tests/test_redis.py
import pytest
from Redis.redis_main import redis_insert_link, redis_get_link
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId


@pytest.mark.asyncio
async def test_redis_insert_and_get():
    # Тестовые данные
    url = "https://redis-test.com"
    short_id = "redis123"

    # Вставка
    await redis_insert_link(LongUrl(url=url), short_id)

    # Получение
    result = await redis_get_link(ShortLinkId(id=short_id))
    assert result.url == url

    # Проверка отсутствия
    result = await redis_get_link(ShortLinkId(id="nonexistent"))
    assert result is None