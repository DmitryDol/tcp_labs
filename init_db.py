import asyncio
from database import create_tables
import orm_models

async def main():
    await create_tables()
   
if __name__ == "__main__":
    asyncio.run(main())
