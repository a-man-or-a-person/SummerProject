import os
import pathlib

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from Pydantic_dir.pydantic_valid_classes import settings

load_dotenv()
if os.getenv("POSTG"):
    print("POSTGRES DB")
else:
    # Create absolute path and ensure directory exists
    db_path = pathlib.Path("DB/links.db").absolute()
    db_path.parent.mkdir(parents=True, exist_ok=True)  # Create directory

    # Use string representation of path with forward slashes
    async_engine = create_async_engine(
        url=f"sqlite+aiosqlite:///{db_path.as_posix()}",
        echo=(settings.test_mode == "True"),
    )

async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
