from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from api.dependencies.dependencies import UOWDep, UserDep
from api.dependencies.pagination_dependency import PaginationDep
from dto import (
    PaginatedRoadmapsDTO,
    UserRoadmapAddExtendedDTO,
    UserRoadmapEditDTO,
)
from services.roadmaps import RoadmapsService
from services.user_cards import UserCardService
from services.user_roadmaps import UserRoadmapsService

router = APIRouter(prefix="/user_roadmaps", tags=["user_roadmaps"])


@router.get("", response_model=PaginatedRoadmapsDTO)
async def get_linked_roadmaps(
    user_dep: UserDep,
    pagination: PaginationDep,
    search: str,
    difficulty: str,
    uow: UOWDep,
):
    roadmaps = await UserRoadmapsService.get_linked_roadmaps(
        uow=uow,
        user_id=user_dep["id"],
        search=search,
        difficulty=difficulty,
        pagination=pagination,
    )

    return roadmaps


@router.post("/{roadmap_id}", response_model=UserRoadmapAddExtendedDTO)
async def link_user_to_roadmap(
    user_dep: UserDep, roadmap_id: Annotated[int, Path(title="Roadmap id")], uow: UOWDep
):
    roadmap = await RoadmapsService.get_roadmap(uow, roadmap_id)

    if roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    user_roadmap_info = await UserRoadmapsService.get_background(
        uow, {"user_id": user_dep["id"], "roadmap_id": roadmap_id}
    )
    if user_roadmap_info is None:
        raise HTTPException(status_code=409, detail="User roadmap relation already exist")

    user_roadmap_id = await UserRoadmapsService.link_user_to_roadmap(
        uow, roadmap_id, user_dep["id"]
    )
    card_ids = await UserCardService.link_user_to_cards_in_roadmap(
        uow, user_dep["id"], roadmap_id
    )
    user_roadmap_id_with_card_ids = {
        "user_id": user_roadmap_id.user_id,
        "roadmap_id": user_roadmap_id.roadmap_id,
        "card_ids": card_ids,
    }
    return UserRoadmapAddExtendedDTO.model_validate(
        user_roadmap_id_with_card_ids, from_attributes=True
    )


@router.delete("/{roadmap_id}", status_code=204)
async def delete_user_roadmap_link(
    user_dep: UserDep, roadmap_id: Annotated[int, Path(title="Roadmap id")], uow: UOWDep
):
    roadmap_info = await RoadmapsService.get_roadmap(uow, roadmap_id)

    if roadmap_info is None:
        raise HTTPException(
            status_code=404, detail=f"Roadmap with id: {roadmap_id} not found"
        )

    if roadmap_info.owner_id == user_dep["id"]:
        await RoadmapsService.delete_roadmap(uow, roadmap_id)
    else:
        await UserRoadmapsService.delete_user_roadmap(
            uow, {"roadmap_id": roadmap_id, "user_id": user_dep["id"]}
        )


@router.get("/{roadmap_id}/background")
async def get_roadmap_background(
    user_dep: UserDep, roadmap_id: Annotated[int, Path(title="Roadmap id")], uow: UOWDep
):
    background = await UserRoadmapsService.get_background(
        uow, {"user_id": user_dep["id"], "roadmap_id": roadmap_id}
    )

    if background is None:
        raise HTTPException(status_code=404, detail="User roadmap relation not found")

    return background


@router.put("/{roadmap_id}/background")
async def edit_roadmap_background(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    background: str,
    uow: UOWDep,
):
    roadmap = await RoadmapsService.get_roadmap(uow, roadmap_id)

    if roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    user_roadmap = await UserRoadmapsService.get_background(
        uow, {"user_id": user_dep["id"], "roadmap_id": roadmap_id}
    )
    if user_roadmap is None:
        raise HTTPException(status_code=404, detail="User roadmap relation not found")

    await UserRoadmapsService.change_background(
        uow,
        roadmap_id,
        user_dep["id"],
        UserRoadmapEditDTO.model_validate(background=background, from_attributes=True),
    )
