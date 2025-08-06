from pydantic import BaseModel, AnyHttpUrl
from pydantic_settings import BaseSettings


class LongUrl(BaseModel):
    url: AnyHttpUrl


class ShortLinkId(BaseModel):
    id: str


class Settings(BaseSettings):
    exp_time: int = 3600  # Default 1 hour
    test_mode: bool = False
    short_id_length: int = 7

    class Config:
        env_file = ".env"


settings = Settings()
