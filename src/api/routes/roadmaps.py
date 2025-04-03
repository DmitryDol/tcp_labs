from typing import Annotated, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from services.user_roadmaps import UserRoadmapsService
from dto import RoadmapAddDTO, RoadmapEditDTO, CardAddDTO, CardEditDTO, CardLinkAddDTO, CardLinkEditDTO, UserRoadmapEditDTO
from api.dependencies import UOWDep
from services.roadmaps import RoadmapsService
from services.cards import CardsService
from services.card_links import card_linksService

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
    card = await CardsService.get_card_extended(uow, card_id)
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

@router.post("/{roadmap_id}/link")
async def link_user_to_roadmap(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    user_id: int,
    uow: UOWDep
):
    await RoadmapsService.link_user_to_roadmap(uow, roadmap_id, user_id)
    return {"roadmap_id": roadmap_id, "user_id": user_id}

@router.delete("/{roadmap_id}/users/{user_id}")
async def delete_user_roadmap_link(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    user_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    await UserRoadmapsService.delete_user_roadmap(uow, {"roadmap_id": roadmap_id, "user_id": user_id})

@router.put("/{roadmap_id}/background")
async def edit_roadmap_background(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    user_id: int,
    background: str,
    uow: UOWDep
):
    await RoadmapsService.change_background(uow, roadmap_id, user_id, UserRoadmapEditDTO(background=background))

@router.delete(
        "/{roadmap_id}/cards/{card_id}/card_links/{card_link_id}",
        status_code=204
)
async def delete_card_link(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    card_id: Annotated[int, Path(title="Card id")],
    card_link_id: Annotated[int, Path(title="Link id")],
    uow: UOWDep
):
    await card_linksService.delete_card_link(uow, card_link_id)

@router.patch("/{roadmap_id}/cards/{card_id}/card_links/{card_link_id}")
async def edit_card_link(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    card_id: Annotated[int, Path(title="Card id")],
    card_link_id: Annotated[int, Path(title="Link id")],
    card_link: CardLinkEditDTO,
    uow: UOWDep
):
    await card_linksService.edit_card_link(uow, card_link_id, card_link)
    return {"card_link_id": card_link_id}


@router.post("/{roadmap_id}/cards/{card_id}/card_links")
async def add_card_link(
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    card_id: Annotated[int, Path(title="Card id")],
    card_link: CardLinkAddDTO,
    uow: UOWDep,
):
    card_link.card_id = card_id
    card_link_id = await CardsService.add_card(uow, card_link)
    return {"card_id": card_link_id}