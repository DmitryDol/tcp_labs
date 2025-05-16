from typing import Annotated, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from crud import card
from services.user_roadmaps import UserRoadmapsService
from dto import RoadmapAddDTO, RoadmapEditDTO, CardAddDTO, CardEditDTO, CardLinkAddDTO, CardLinkEditDTO, UserRoadmapEditDTO
from api.dependencies.dependencies import UOWDep, UserDep
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
    card_link_id = await CardLinksService.delete_card_link(uow, card_link_id)
    if card_link_id is None:
        raise HTTPException(status_code=404, detail='Card link not found')

@router.patch("/{card_link_id}")
async def edit_card_link(
    user_dep: UserDep,
    card_link_id: Annotated[int, Path(title="Link id")],
    card_link: CardLinkEditDTO,
    uow: UOWDep
):
    curr_card_link = await CardLinksService.get_card_link(uow, card_link_id)

    if curr_card_link is None:
        raise HTTPException(status_code=404, detail='Card link not found')
    
    card_id = (await CardLinksService.get_card_links(uow)).card_id
    roadmap_id = (await CardsService.get_card(uow, card_id)).roadmap_id
    roadmap = await RoadmapsService.get_roadmap(uow, roadmap_id)

    if roadmap.owner_id != user_dep['id'] and roadmap.edit_permission != 'can edit':
        raise HTTPException(status_code=403, detail='User does not have permission to edit card link to this roadmap')

    card_link_id = await CardLinksService.edit_card_link(uow, card_link_id, card_link)
    return {"card_link_id": card_link_id}


@router.post("")
async def add_card_link(
    user_dep: UserDep,
    card_link: CardLinkAddDTO,
    uow: UOWDep,
):
    card_info = await CardsService.get_card(uow, card_link.card_id)

    if card_info is None:
        raise HTTPException(status_code=404, detail='Card not found')
        
    roadmap_info = await RoadmapsService.get_roadmap(uow, card_info.roadmap_id)
    
    if roadmap_info.owner_id != user_dep['id'] and roadmap_info.edit_permission != "can edit":
        raise HTTPException(status_code=403, detail='User does not have permission to add card link to this roadmap')

    card_link_id = await CardLinksService.add_card_link(uow, card_link)
    return {"card_link_id": card_link_id}