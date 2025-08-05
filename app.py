import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from test_db.orm import insert_link, get_long_link
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId

app = FastAPI()


@app.get('/ping', status_code=status.HTTP_200_OK)
async def ping():
    return {'Ping': 'ok'}


@app.post('/get_short', status_code=status.HTTP_201_CREATED)
async def url_conv(user_url: LongUrl):
    try:
        short_link_id = await insert_link(user_url)
        short_link = f'https://localhost:8003/red/{short_link_id}'
        return short_link
    except Exception as e:
        print(e)
        return {
            'Error': e
        }


@app.get('/red/{red_id}')
async def redirection(red_id: int):
    red_id = ShortLinkId(id=red_id)
    link = await get_long_link(red_id)
    return RedirectResponse(url=str(link.url), status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="localhost",  # Accessible on all network interfaces
        port=8003,  # Default FastAPI port
        reload=True  # Enable auto-reload during development
    )



