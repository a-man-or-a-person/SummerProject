import asyncio
from test_db.orm import create_tables

if __name__ == '__main__':
    asyncio.run(create_tables())
