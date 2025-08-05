import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from functions import convert_long_link, get_long_link
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId
from Redis.redis_main import redis_get_link, redis_insert_link

load_dotenv()
app = FastAPI()


@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    return {"Ping": "ok"}


@app.post("/get_short", status_code=status.HTTP_201_CREATED)
async def url_conv(user_url: LongUrl):
    try:
        short_link_id = await convert_long_link(user_url)
        short_link = f"https://localhost:8003/red/{short_link_id}"
        return short_link
    except Exception as e:
        print(e)
        return {"Error": e}


@app.get("/red/{red_id}")
async def redirection(red_id: int):
    red_id = ShortLinkId(id=red_id)
    link = await get_long_link(red_id)
    if os.getenv("TEST") == "True":
        return str(link.url)
    else:
        return RedirectResponse(url=str(link.url), status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="localhost",  # Accessible on all network interfaces
        port=8003,  # Default FastAPI port
        reload=True,  # Enable auto-reload during development
    )
