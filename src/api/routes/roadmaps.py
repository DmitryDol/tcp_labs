from typing import Annotated, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from services.user_roadmaps import UserRoadmapsService
from dto import RoadmapAddDTO, RoadmapEditDTO, CardAddDTO, CardEditDTO, CardLinkAddDTO, CardLinkEditDTO, UserRoadmapEditDTO
from api.dependencies import UOWDep, UserDep
from services.roadmaps import RoadmapsService
from services.cards import CardsService
from services.card_links import CardLinksService

router = APIRouter(
    prefix="/roadmaps", 
    tags=["roadmaps"]
)


@router.get("")
async def get_public_roadmaps(
    user_dep: UserDep,
    uow: UOWDep,
    search: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 0
):
    roadmaps = await RoadmapsService.get_public_roadmaps(uow, search, difficulty, limit)
    return roadmaps
    

@router.post("")
async def add_roadmap(
    user_dep: UserDep,
    roadmap: RoadmapAddDTO,
    uow: UOWDep
):
    roadmap_id, user_id = await RoadmapsService.add_roadmap(uow, roadmap)
    return {"roadmap_id": roadmap_id, "user_id": user_id}

@router.get("/{roadmap_id}")
async def get_roadmap_info(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    extended_roadmap = await RoadmapsService.get_roadmap_extended(uow, roadmap_id)
    return extended_roadmap

@router.patch("/{roadmap_id}")
async def edit_roadmap(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    roadmap: RoadmapEditDTO,
    uow: UOWDep
):
    await RoadmapsService.edit_roadmap(uow, roadmap_id, roadmap)
    return {"roadmap_id": roadmap_id}

@router.delete(
        "/{roadmap_id}",
        status_code=204
)
async def delete_roadmap(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    await RoadmapsService.delete_roadmap(uow, roadmap_id)

@router.post("/{roadmap_id}/link")
async def link_user_to_roadmap(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    await RoadmapsService.link_user_to_roadmap(uow, roadmap_id, user_dep['id'])
    return {"roadmap_id": roadmap_id, "user_id": user_dep['id']}

@router.delete(
        "/{roadmap_id}/users/{user_id}",
        status_code=204
)
async def delete_user_roadmap_link(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    user_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    await UserRoadmapsService.delete_user_roadmap(uow, {"roadmap_id": roadmap_id, "user_id": user_id})

@router.put("/{roadmap_id}/background")
async def edit_roadmap_background(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    user_id: int,
    background: str,
    uow: UOWDep
):
    await RoadmapsService.change_background(uow, roadmap_id, user_id, UserRoadmapEditDTO(background=background))

