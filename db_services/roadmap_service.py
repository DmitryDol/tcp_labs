from sqlalchemy import text, insert
from src.database import async_session_factory, async_engine
from src.models import Roadmap
import asyncio


async def insert_data(data):
    async with async_engine.connect() as conn:
        stmt = insert(Roadmap).values(data)
        await conn.execute(stmt)
        await conn.commit()

data = [{"title":"Алгоритмы и структуры данных",
                "description":"Руководство по изучению базовых и продвинутых алгоритмов для эффективного программирования.",
                "difficulty":Roadmap.DifficultyEnum.medium}]

if __name__ == "__main__":
    asyncio.run(insert_data(data))