from fastapi import APIRouter

from api.routes import auth, card_links, cards, roadmaps, user_cards, user_roadmaps, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(roadmaps.router)
api_router.include_router(user_roadmaps.router)
api_router.include_router(cards.router)
api_router.include_router(card_links.router)
api_router.include_router(user_cards.router)
