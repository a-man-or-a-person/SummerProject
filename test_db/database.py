import pathlib
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from Pydantic_dir.pydantic_valid_classes import settings

pathlib.Path('.data').mkdir(exist_ok=True)
async_engine = create_async_engine(settings.database_url, poolclass=NullPool)
async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass
