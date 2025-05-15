from typing import Annotated, List, Optional
from fastapi import APIRouter, HTTPException, Path
from dto import SimplifiedRoadmapDTO, UserRoadmapAddDTO, UserRoadmapDTO, UserRoadmapEditDTO
from services.user_roadmaps import UserRoadmapsService
from api.dependencies import UOWDep, UserDep
from services.roadmaps import RoadmapsService

router = APIRouter(
    prefix="/user_roadmaps", 
    tags=["user_roadmaps"]
)


@router.get("", response_model=List[SimplifiedRoadmapDTO])
async def get_linked_roadmaps(
    user_dep: UserDep,
    search: str,
    difficulty: str,
    uow: UOWDep,
    limit: Optional[int] = 0
):
    roadmaps = await UserRoadmapsService.get_linked_roadmaps(
        uow=uow, 
        user_id=user_dep['id'], 
        search=search, 
        difficulty=difficulty, 
        limit=limit
    )

    return roadmaps

@router.post("/{roadmap_id}", response_model=UserRoadmapAddDTO)
async def link_user_to_roadmap(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    user_roadmap_id = await UserRoadmapsService.link_user_to_roadmap(uow, roadmap_id, user_dep['id'])
    return user_roadmap_id

@router.delete(
        "/{roadmap_id}",
        status_code=204
)
async def delete_user_roadmap_link(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    roadmap_info = await RoadmapsService.get_roadmap(uow, roadmap_id)
    if roadmap_info is None:
        raise HTTPException(status_code=404, detail=f'Roadmap with id: {roadmap_id} not found')
    if roadmap_info.owner_id == user_dep['id']:
        await RoadmapsService.delete_roadmap(uow, roadmap_id)
    else:
        await UserRoadmapsService.delete_user_roadmap(uow, {"roadmap_id": roadmap_id, "user_id": user_dep['id']})

@router.get("/{roadmap_id}/background", response_model=UserRoadmapDTO)
async def get_roadmap_background(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    uow: UOWDep
):
    background = await UserRoadmapsService.get_background(uow, {"user_id": user_dep['id'], "roadmap_id": roadmap_id})
    return background

@router.put("/{roadmap_id}/background")
async def edit_roadmap_background(
    user_dep: UserDep,
    roadmap_id: Annotated[int, Path(title="Roadmap id")],
    background: str,
    uow: UOWDep
):
    await UserRoadmapsService.change_background(uow, roadmap_id, user_dep['id'], UserRoadmapEditDTO.model_validate(background=background, from_attributes=True))

