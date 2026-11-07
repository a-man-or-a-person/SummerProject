from unittest.mock import AsyncMock
import pytest
from redis.exceptions import ConnectionError
import functions
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId

@pytest.mark.asyncio
async def test_identifiers_are_deterministic_and_fixed_length():
    ids = [await functions.gen_short_id(LongUrl(url=f'https://example.com/{i}')) for i in range(100)]
    assert len(set(ids)) == 100
    assert all(len(value) == 7 for value in ids)
    assert ids[0] == await functions.gen_short_id(LongUrl(url='https://example.com/0'))

@pytest.mark.asyncio
async def test_failed_database_write_never_populates_cache(monkeypatch):
    cache = AsyncMock()
    monkeypatch.setattr(functions, 'insert_link', AsyncMock(side_effect=RuntimeError('DB unavailable')))
    monkeypatch.setattr(functions, 'redis_insert_link', cache)
    with pytest.raises(RuntimeError):
        await functions.convert_long_link(LongUrl(url='https://example.com'))
    cache.assert_not_awaited()

@pytest.mark.asyncio
async def test_cache_outage_preserves_durable_round_trip(monkeypatch):
    monkeypatch.setattr(functions, 'redis_insert_link', AsyncMock(side_effect=ConnectionError()))
    monkeypatch.setattr(functions, 'redis_get_link', AsyncMock(side_effect=ConnectionError()))
    url = LongUrl(url='https://example.com/outage')
    short_id = await functions.convert_long_link(url)
    assert await functions.get_long_link(ShortLinkId(id=short_id)) == url
