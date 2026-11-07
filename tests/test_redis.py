from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId
from Redis.redis_main import redis_get_link, redis_insert_link

@pytest.mark.asyncio
async def test_cache_serialization_and_missing_key():
    redis = AsyncMock()
    redis.get.side_effect = [b'https://example.com/', None]
    manager = MagicMock()
    manager.__aenter__ = AsyncMock(return_value=redis)
    manager.__aexit__ = AsyncMock(return_value=False)
    with patch('Redis.redis_main.Redis', return_value=manager):
        await redis_insert_link(LongUrl(url='https://example.com'), 'id')
        assert await redis_get_link(ShortLinkId(id='id')) == LongUrl(url='https://example.com')
        assert await redis_get_link(ShortLinkId(id='missing')) is None
    redis.setex.assert_awaited_once()
