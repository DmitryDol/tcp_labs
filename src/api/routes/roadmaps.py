from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from api.dependencies.dependencies import UOWDep, UserDep
from api.dependencies.pagination_dependency import PaginationDep
from dto import (
    PaginatedRoadmapsDTO,
    RoadmapAddDTO,
    RoadmapDTO,
    RoadmapEditDTO,
    RoadmapExtendedDTO,
)
from services.roadmaps import RoadmapsService
from services.user_roadmaps import UserRoadmapsService

router = APIRouter(prefix="/roadmaps", tags=["roadmaps"])


@router.get("/public", response_model=PaginatedRoadmapsDTO)
async def get_public_roadmaps(
    # user_dep: UserDep,
    uow: UOWDep,
    pagination: PaginationDep,
    search: str | None = None,
    difficulty: str | None = None,
):
    roadmaps = await RoadmapsService.get_public_roadmaps(
        uow, pagination, search, difficulty
    )
    return roadmaps


@router.post("")
async def add_roadmap(user_dep: UserDep, roadmap: RoadmapAddDTO, uow: UOWDep):
    roadmap.owner_id = user_dep["id"]
    roadmap_id, user_id = await RoadmapsService.add_roadmap(uow, roadmap)
    await UserRoadmapsService.link_user_to_roadmap(uow, roadmap_id, user_id)
    return {"roadmap_id": roadmap_id, "user_id": user_id}


@router.get("/{roadmap_id}", response_model=RoadmapExtendedDTO)
async def get_roadmap_info(
    user_dep: UserDep, roadmap_id: Annotated[int, Path(title="Roadmap id")], uow: UOWDep
):
    extended_roadmap = await RoadmapsService.get_roadmap_extended(uow, roadmap_id)

    if extended_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if (
        extended_roadmap.owner_id != user_dep["id"]
        and extended_roadmap.visibility == "private"
    ):
        raise HTTPException(status_code=403, detail="Roadmap is private")

    return extended_roadmap


@router.patch("/{roadmap_id}")
async def edit_roadmap(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    roadmap: RoadmapEditDTO,
    uow: UOWDep,
):
    roadmap_info: RoadmapDTO | None = await RoadmapsService.get_roadmap(uow, roadmap_id)

    if roadmap_info is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if (
        roadmap_info.owner_id != user_dep["id"]
        and roadmap_info.edit_permission != "can edit"
    ):
        raise HTTPException(
            status_code=403,
            detail="The user does not have permission to edit this roadmap",
        )

    await RoadmapsService.edit_roadmap(uow, roadmap_id, roadmap)
    return {"roadmap_id": roadmap_id}


@router.delete("/{roadmap_id}", status_code=204)
async def delete_roadmap(
    user_dep: UserDep, roadmap_id: Annotated[int, Path(title="Roadmap id")], uow: UOWDep
):
    roadmap = await RoadmapsService.get_roadmap(uow, roadmap_id)

    if roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if roadmap.owner_id != user_dep["id"]:
        raise HTTPException(
            status_code=403,
            detail="The user does not have permission to delete this roadmap",
        )
    await RoadmapsService.delete_roadmap(uow, roadmap_id)
