import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from DB.main_db import add_link
from Pydantic_dir.pydantic_valid_classes import LongUrl

app = FastAPI()


@app.get('/ping', status_code=status.HTTP_200_OK)
async def ping():
    return {'Ping': 'ok'}


@app.post('/get_short', status_code=status.HTTP_201_CREATED)
async def url_conv(url: LongUrl):
    return {
        'Done': 'ok'
    }


@app.get('/red/{red_id}', status_code=status.HTTP_200_OK)
async def redirection(red_id: int):
    print(red_id)
    return RedirectResponse(url='/docs', status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="localhost",  # Accessible on all network interfaces
        port=8003,  # Default FastAPI port
        reload=True  # Enable auto-reload during development
    )
