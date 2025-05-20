from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from api.dependencies.dependencies import UOWDep, UserDep
from dto import CardAddDTO, CardEditDTO, CardExtendedDTO, RoadmapDTO
from services.cards import CardsService
from services.roadmaps import RoadmapsService

router = APIRouter(prefix="/cards", tags=["cards"])


@router.post("")
async def add_card(
    user_dep: UserDep,
    card: CardAddDTO,
    uow: UOWDep,
):
    roadmap_info: RoadmapDTO | None = await RoadmapsService.get_roadmap(
        uow, card.roadmap_id
    )

    if roadmap_info is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if (
        roadmap_info.owner_id != user_dep["id"]
        and roadmap_info.edit_permission != "can edit"
    ):
        raise HTTPException(
            status_code=403, detail="User does not have permission to edit this card."
        )

    card_id = await CardsService.add_card(uow, card)
    return {"card_id": card_id}


@router.get("/{card_id}", response_model=CardExtendedDTO)
async def get_card_info(
    user_dep: UserDep, card_id: Annotated[int, Path(title="Card id")], uow: UOWDep
):
    card = await CardsService.get_card_extended(uow, card_id)

    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    roadmap_info = await RoadmapsService.get_roadmap(uow, card.roadmap_id)

    if roadmap_info.owner_id != user_dep["id"] and roadmap_info.visibility == "private":
        raise HTTPException(
            status_code=403,
            detail="User does not have permission to view card of this roadmap",
        )

    return card


@router.delete("/{card_id}", status_code=204)
async def delete_card(
    user_dep: UserDep, card_id: Annotated[int, Path(title="Card id")], uow: UOWDep
):
    card = await CardsService.get_card(uow, card_id)

    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    roadmap_info = await RoadmapsService.get_roadmap(uow, card.roadmap_id)

    if (
        roadmap_info.owner_id != user_dep["id"]
        and roadmap_info.edit_permission != "can edit"
    ):
        raise HTTPException(
            status_code=403,
            detail="User does not have permission to view card of this roadmap",
        )

    await CardsService.delete_card(uow, card_id)


@router.patch("/{card_id}")
async def edit_card(
    user_dep: UserDep,
    card_id: Annotated[int, Path(title="Card id")],
    card: CardEditDTO,
    uow: UOWDep,
):
    card_info = await CardsService.get_card(uow, card_id)

    if card_info is None:
        raise HTTPException(status_code=404, detail="Card not found")

    roadmap_info = await RoadmapsService.get_roadmap(uow, card.roadmap_id)

    if (
        roadmap_info.owner_id != user_dep["id"]
        and roadmap_info.edit_permission != "can edit"
    ):
        raise HTTPException(
            status_code=403,
            detail="User does not have permission to view card of this roadmap",
        )

    await CardsService.edit_card(uow, card_id, card)
    return {"card_id": card_id}
