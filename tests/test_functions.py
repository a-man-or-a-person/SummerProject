# tests/test_functions.py
import pytest

from functions import gen_short_id
from Pydantic_dir.pydantic_valid_classes import LongUrl


def test_gen_short_id_same_url():
    url = LongUrl(url="https://example.com")
    id1 = gen_short_id(str(url.url))
    id2 = gen_short_id(str(url.url))
    assert id1 == id2


def test_gen_short_id_different_urls():
    id1 = gen_short_id("https://example1.com")
    id2 = gen_short_id("https://example2.com")
    assert id1 != id2


def test_gen_short_id_length():
    url = LongUrl(url="https://example.com")
    short_id = gen_short_id(str(url.url))
    assert len(short_id) == 7  # SHORT_ID_LENGTH по умолчанию
