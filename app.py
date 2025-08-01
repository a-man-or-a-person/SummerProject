from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from Pydantic_dir.pydantic_valid_classes import LongUrl

app = FastAPI()


@app.get('/ping', status_code=status.HTTP_200_OK)
def ping():
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
