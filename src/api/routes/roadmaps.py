<<<<<<< HEAD
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from dto import RoadmapAddDTO, RoadmapEditDTO, CardAddDTO, CardEditDTO
=======
from typing import Annotated
from fastapi import APIRouter, Path
from dto import RoadmapAddDTO, RoadmapEditDTO
>>>>>>> 560fd71992f487f17c2d0c6ab9228cbd16038261
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
@router.post("")
async def add_roadmap(
    roadmap: RoadmapAddDTO,
    uow: UOWDep
):
    roadmap_id, user_id = await RoadmapsService.add_roadmap(uow, roadmap)
    return {"roadmap_id": roadmap_id, "user_id": user_id}

@router.get("/{roadmap_id}")
async def get_roadmap_info(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    extended_roadmap = await RoadmapsService.get_roadmap_extended(uow, roadmap_id)
    return extended_roadmap

@router.patch("/{roadmap_id}")
async def edit_roadmap(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    roadmap: RoadmapEditDTO,
    uow: UOWDep
):
    await RoadmapsService.edit_roadmap(uow, roadmap_id, roadmap)
    return {"roadmap_id": roadmap_id}

@router.delete("/{roadmap_id}")
async def delete_roadmap(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    await RoadmapsService.delete_roadmap(uow, roadmap_id)
