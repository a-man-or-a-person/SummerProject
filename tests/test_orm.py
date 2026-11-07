import asyncio
import pytest
from fastapi import HTTPException
from test_db.orm import insert_link, get_long_link_db
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId

@pytest.mark.asyncio
async def test_concurrent_duplicate_writes_are_idempotent():
    url = LongUrl(url='https://example.com/concurrent')
    await asyncio.gather(insert_link(url, 'same'), insert_link(url, 'same'))
    assert await get_long_link_db(ShortLinkId(id='same')) == url

@pytest.mark.asyncio
async def test_collision_keeps_original_destination():
    original = LongUrl(url='https://example.com/original')
    await insert_link(original, 'collision')
    with pytest.raises(HTTPException) as error:
        await insert_link(LongUrl(url='https://example.com/other'), 'collision')
    assert error.value.status_code == 409
    assert await get_long_link_db(ShortLinkId(id='collision')) == original
