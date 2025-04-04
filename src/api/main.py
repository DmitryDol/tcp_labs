from fastapi import APIRouter

from api.routes import roadmaps, users
from config import settings

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(roadmaps.router)