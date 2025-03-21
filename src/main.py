import asyncio
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from src.queries.orm import AsyncORM


async def main():
    # await AsyncORM.create_tables()
    await AsyncORM.drop_tables()

if __name__ == "__main__":
    asyncio.run(main())