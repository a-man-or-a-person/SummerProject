from pydantic import AnyUrl, BaseModel


class LongUrl(BaseModel):
    url: AnyUrl


class ShortLinkId(BaseModel):
    id: int
