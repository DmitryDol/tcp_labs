from typing import Annotated, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from dto import RoadmapAddDTO, RoadmapEditDTO, CardAddDTO, CardEditDTO
from api.dependencies import UOWDep
from services.roadmaps import RoadmapsService
from services.cards import CardsService

router = APIRouter(
    prefix="/roadmaps", 
    tags=["roadmaps"]
)


@router.get("")
async def get_public_roadmaps(
    search: str,
    difficulty: str,
    uow: UOWDep,
    limit: int = 0
):
    roadmaps = await RoadmapsService.get_public_roadmaps(uow, search, difficulty, limit)
    return roadmaps
    
@router.post("/{roadmap_id}/cards")
async def add_card(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    card: CardAddDTO,
    uow: UOWDep,
):
    card.roadmap_id = roadmap_id
    card_id = await CardsService.add_card(uow, card)
    return {"card_id": card_id}

@router.get("/{roadmap_id}/cards/{cars_id}")
async def get_card_info(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    card_id: Annotated[int, Path(title="Card id")],
    uow: UOWDep
):
    card = await CardsService.get_cards(uow=uow, filter_by=card_id)
    return card

@router.delete(
        "/{roadmap_id}/cards",
        status_code=204
)
async def delete_card(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    card_id: int,
    uow: UOWDep
):
    await CardsService.delete_card(uow, card_id)

@router.patch("/{roadmap_id}/cards/{card_id}")
async def edit_card(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    card_id: Annotated[int, Path(title="Card id")],
    card: CardEditDTO,
    uow: UOWDep
):
    await CardsService.edit_card(uow, card_id, card)
    return {"card_id": card_id}