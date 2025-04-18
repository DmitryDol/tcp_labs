from typing import Annotated
from fastapi import APIRouter, HTTPException, Path
from dto import UserAddDTO, UserEditDTO
from api.dependencies import UOWDep, UserDep
from services.users import UsersService


router = APIRouter(
    prefix="/users", 
    tags=["users"]
)

@router.get("/{user_id}")
async def get_user_info(
    user_dep: UserDep,
    user_id: Annotated[int, Path(title="User id")],
    uow: UOWDep
):
    user = await UsersService.get_user(uow=uow, filter_by=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete(
        "/{user_id}",
        status_code=204
)
async def delete_user(
    user_dep: UserDep,
    uow: UOWDep
):
    await UsersService.delete_user(uow, user_dep['id'])

@router.patch("/{user_id}")
async def edit_user(
    user_dep: UserDep,
    user: UserEditDTO,
    uow: UOWDep
):
    await UsersService.edit_user(uow, user_dep['id'], user)
    return {"user_id": user_dep['id']}

@router.get("/{user_id}/roadmaps")
async def get_linked_roadmaps(
    user_dep: UserDep,
    search: str,
    difficulty: str,
    uow: UOWDep,
    limit: int = 0
):
    roadmaps = await UsersService.get_linked_roadmaps(
        uow=uow, 
        search=search, 
        difficulty=difficulty, 
        limit=limit, 
        user_id=user_dep['id']
    )

    return roadmaps