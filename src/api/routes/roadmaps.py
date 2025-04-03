from typing import Annotated
from fastapi import APIRouter, Path
from dto import RoadmapAddDTO, RoadmapEditDTO
from api.dependencies import UOWDep
from services.roadmaps import RoadmapsService

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