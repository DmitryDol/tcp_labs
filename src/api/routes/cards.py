from typing import Annotated, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from services.user_roadmaps import UserRoadmapsService
from dto import RoadmapAddDTO, RoadmapEditDTO, CardAddDTO, CardEditDTO, CardLinkAddDTO, CardLinkEditDTO, UserRoadmapEditDTO
from api.dependencies import UOWDep, UserDep
from services.roadmaps import RoadmapsService
from services.cards import CardsService
from services.card_links import CardLinksService

router = APIRouter(
    prefix="/cards", 
    tags=["cards"]
)

@router.post("")
async def add_card(
    user_dep: UserDep,
    roadmap_id: int,
    card: CardAddDTO,
    uow: UOWDep,
):
    card.roadmap_id = roadmap_id
    card_id = await CardsService.add_card(uow, card)
    return {"card_id": card_id}

@router.get("/{card_id}")
async def get_card_info(
    user_dep: UserDep,
    card_id: Annotated[int, Path(title="Card id")],
    uow: UOWDep
):
    card = await CardsService.get_card_extended(uow, card_id)
    return card

@router.delete(
        "/{card_id}",
        status_code=204
)
async def delete_card(
    user_dep: UserDep,
    card_id: Annotated[int, Path(title="Card id")],
    uow: UOWDep
):
    await CardsService.delete_card(uow, card_id)

@router.patch("/{card_id}")
async def edit_card(
    user_dep: UserDep,
    card_id: Annotated[int, Path(title="Card id")],
    card: CardEditDTO,
    uow: UOWDep
):
    await CardsService.edit_card(uow, card_id, card)
    return {"card_id": card_id}