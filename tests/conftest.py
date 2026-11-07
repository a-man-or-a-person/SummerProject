import asyncio
import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock
import pytest
from fastapi.testclient import TestClient

_database = tempfile.TemporaryDirectory()
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///' + (Path(_database.name) / 'test.db').as_posix()

from app import app
import functions
from test_db.orm import create_tables
from test_db.database import async_engine

@pytest.fixture(autouse=True)
def isolated_storage(monkeypatch):
    asyncio.run(create_tables())
    monkeypatch.setattr(functions, 'redis_get_link', AsyncMock(return_value=None))
    monkeypatch.setattr(functions, 'redis_insert_link', AsyncMock())
    yield
    asyncio.run(async_engine.dispose())

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
