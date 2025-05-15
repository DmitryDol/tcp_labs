from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from api.dependencies.pagination_dependency import PaginationDep
from services.user_roadmaps import UserRoadmapsService
from dto import RoadmapAddDTO, RoadmapDTO, RoadmapEditDTO, CardAddDTO, CardEditDTO, CardLinkAddDTO, CardLinkEditDTO, RoadmapExtendedDTO, UserRoadmapEditDTO
from api.dependencies.dependencies import UOWDep, UserDep
from services.roadmaps import RoadmapsService
from services.cards import CardsService
from services.card_links import CardLinksService

router = APIRouter(
    prefix="/roadmaps", 
    tags=["roadmaps"]
)


@router.get("/public", response_model=List[RoadmapDTO])
async def get_public_roadmaps(
    # user_dep: UserDep,
    uow: UOWDep,
    pagination: PaginationDep,
    search: Optional[str] = None,
    difficulty: Optional[str] = None
):
    roadmaps = await RoadmapsService.get_public_roadmaps(uow, pagination, search, difficulty)
    return roadmaps
    

@router.post("")
async def add_roadmap(
    user_dep: UserDep,
    roadmap: RoadmapAddDTO,
    uow: UOWDep
):
    roadmap_id, user_id = await RoadmapsService.add_roadmap(uow, roadmap)
    await UserRoadmapsService.link_user_to_roadmap(uow, roadmap_id, user_id)
    return {"roadmap_id": roadmap_id, "user_id": user_id}

@router.get("/{roadmap_id}", response_model=RoadmapExtendedDTO)
async def get_roadmap_info(
    user_dep: Optional[UserDep],
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    extended_roadmap = await RoadmapsService.get_roadmap_extended(uow, roadmap_id)
    if extended_roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    if extended_roadmap.owner_id != user_dep['id'] and extended_roadmap.visibility == 'private':
        raise HTTPException(status_code=403, detail="Roadmap is private")
    return extended_roadmap

@router.patch("/{roadmap_id}")
async def edit_roadmap(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    roadmap: RoadmapEditDTO,
    uow: UOWDep
):
    roadmap_info: RoadmapDTO = RoadmapsService.get_roadmap(uow, roadmap_id)
    if roadmap_info.owner_id != user_dep['id'] and roadmap_info.edit_permission != "can edit":
        raise HTTPException(
            status_code=403, 
            detail='The user does not have permission to edit this roadmap'
        )
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
    roadmap = await RoadmapsService.get_roadmap(uow, roadmap_id)
    if roadmap.owner_id != user_dep['id']:
        raise HTTPException(
            status_code=403, 
            detail='The user does not have permission to delete this roadmap'
        )
    await RoadmapsService.delete_roadmap(uow, roadmap_id)

