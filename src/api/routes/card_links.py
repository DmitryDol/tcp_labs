from typing import Annotated, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from services.user_roadmaps import UserRoadmapsService
from dto import RoadmapAddDTO, RoadmapEditDTO, CardAddDTO, CardEditDTO, CardLinkAddDTO, CardLinkEditDTO, UserRoadmapEditDTO
from api.dependencies import UOWDep, UserDep
from services.roadmaps import RoadmapsService
from services.cards import CardsService
from services.card_links import CardLinksService

router = APIRouter(
    prefix="/card_links", 
    tags=["card_links"]
)


@router.delete(
        "/{card_link_id}",
        status_code=204
)
async def delete_card_link(
    user_dep: UserDep,
    card_link_id: Annotated[int, Path(title="Link id")],
    uow: UOWDep
):
    await CardLinksService.delete_card_link(uow, card_link_id)

@router.patch("/{card_link_id}")
async def edit_card_link(
    user_dep: UserDep,
    card_link_id: Annotated[int, Path(title="Link id")],
    card_link: CardLinkEditDTO,
    uow: UOWDep
):
    await CardLinksService.edit_card_link(uow, card_link_id, card_link)
    return {"card_link_id": card_link_id}


@router.post("")
async def add_card_link(
    user_dep: UserDep,
    card_id: int,
    card_link: CardLinkAddDTO,
    uow: UOWDep,
):
    card_link.card_id = card_id
    card_link_id = await CardLinksService.add_card_link(uow, card_link)
    return {"card_link_id": card_link_id}