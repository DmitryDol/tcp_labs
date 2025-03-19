from sqlalchemy import text, insert
from src.database import async_session_factory, async_engine
from src.models import Card
import asyncio



