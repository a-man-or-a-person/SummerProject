import asyncio

from DB.orm import drop_tables, get_long_link, insert_link

from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId


async def main():
    link = LongUrl(url="https://google.com")
    short_link = ShortLinkId(id=1)
    # await drop_tables()
    # await insert_link(link)
    res = await get_long_link(short_link)
    print("Done: ", res.url)


if __name__ == "__main__":
    asyncio.run(main())
