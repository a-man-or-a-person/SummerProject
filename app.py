from contextlib import asynccontextmanager
from test_db.orm import create_tables
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel

from functions import convert_long_link, get_long_link
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId, settings


# Добавьте эти модели
class ShortLinkResponse(BaseModel):
    short_url: str


class ErrorResponse(BaseModel):
    error: str


load_dotenv()
@asynccontextmanager
async def lifespan(app):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки, в проде укажите домен фронтенда
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    return {"Ping": "ok"}


@app.post(
    path="/get_short",
    status_code=status.HTTP_201_CREATED,
    response_model=ShortLinkResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad Request",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Internal Server Error",
        },
    },
)
async def url_conv(user_url: LongUrl, request: Request):
    try:
        short_link_id = await convert_long_link(user_url)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"short_url": str(request.url_for("redirection", red_id=short_link_id))},
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Server error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@app.get(path="/red/{red_id}")
async def redirection(red_id: str):
    red_id = ShortLinkId(id=red_id)
    link = await get_long_link(red_id)
    return RedirectResponse(url=str(link.url), status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="localhost",  # Accessible on all network interfaces
        port=8003,  # Default FastAPI port
        reload=True,  # Enable auto-reload during development
    )
