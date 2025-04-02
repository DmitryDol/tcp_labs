from fastapi import APIRouter

from src.api.routes import users
from src.config import settings

api_router = APIRouter()
api_router.include_router(users.router)