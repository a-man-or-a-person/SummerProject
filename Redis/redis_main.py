import redis
from Pydantic_dir.pydantic_valid_classes import LongUrl, ShortLinkId
from dotenv import load_dotenv
import os

load_dotenv()
# Connect to local Redis (default settings)
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0,  # Database index (0-15)
    password=None  # If your Redis requires authentication
)


def redis_insert_link(url: LongUrl, short_id: int):
    r.setex(f'{short_id}', int(os.getenv('EXP_TIME')), f'{str(url.url)}')
    print(r.exists(f'{short_id}'))


def redis_get_link():
    r.get()


# Test the connection
print(r.ping())
