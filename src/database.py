from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings
from models import *

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine)


# async_session = sessionmaker(
#    bind=async_engine,
#    class_=AsyncSession,
#    expire_on_commit=False
# )


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
