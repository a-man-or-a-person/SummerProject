from pydantic import BaseModel, AnyUrl


class LongUrl(BaseModel):
    url: AnyUrl


class ShortLinkId(BaseModel):
    id: int
