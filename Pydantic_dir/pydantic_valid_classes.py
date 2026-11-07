from pydantic import AnyHttpUrl, BaseModel, Field
from pydantic_settings import BaseSettings


class LongUrl(BaseModel):
    url: AnyHttpUrl


class ShortLinkId(BaseModel):
    id: str


class Settings(BaseSettings):
    exp_time: int = Field(default=3600, ge=1)  # Default 1 hour
    test_mode: bool = False
    short_id_length: int = Field(default=7, ge=1, le=32)
    database_url: str = "sqlite+aiosqlite:///.data/links.db"
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()
