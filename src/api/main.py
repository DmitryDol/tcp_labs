from fastapi import APIRouter

from api.routes import auth, roadmaps, users, cards, card_links
from config import settings

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(roadmaps.router)
api_router.include_router(cards.router)
api_router.include_router(card_links.router)