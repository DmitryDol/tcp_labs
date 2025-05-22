from fastapi import APIRouter, HTTPException

from api.dependencies.dependencies import UOWDep, UserDep
from dto import UserCardEditDTO, UserCardEditWithUserIdDTO
from services.cards import CardsService
from services.roadmaps import RoadmapsService
from services.user_cards import UserCardService
from services.user_roadmaps import UserRoadmapsService

router = APIRouter(prefix="/user_cards", tags=["user_cards"])


@router.put("/status")
async def change_card_status(
    uow: UOWDep, user_dep: UserDep, user_card: UserCardEditWithUserIdDTO
):
    card_info = await CardsService.get_card(uow, user_card.card_id)

    if card_info is None:
        raise HTTPException(status_code=404, detail="Card not found")

    roadmap_info = await RoadmapsService.get_roadmap(uow, card_info.roadmap_id)

    # TODO check is it neccessary to check permission to change card status
    if roadmap_info.owner_id != user_dep["id"] and roadmap_info.visibility == "private":
        raise HTTPException(
            status_code=403,
            detail="User does not have permission to edit card status to this roadmap",
        )

    user_roadmap_info = await UserRoadmapsService.get_background(
        uow, {"user_id": user_dep["id"], "roadmap_id": roadmap_info.id}
    )
    if user_roadmap_info is None:
        raise HTTPException(
            status_code=400, detail="User not linked to roadmap with this card"
        )

    await UserCardService.edit_user_card(
        uow, {"user_id": user_dep["id"], "card_id": user_card.card_id}, UserCardEditDTO(user_card.status)
    )
