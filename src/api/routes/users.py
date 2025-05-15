from typing import Annotated, Optional
from fastapi import APIRouter, HTTPException, Path
from dto import UserAddDTO, UserDTO, UserEditDTO
from api.dependencies import UOWDep, UserDep
from services.users import UsersService


router = APIRouter(
    prefix="/users", 
    tags=["users"]
)

@router.get("", response_model=UserDTO)
async def get_user_info(
    user_dep: UserDep,
    uow: UOWDep
):
    user = await UsersService.get_user(uow=uow, filter_by=user_dep['id'])
    return user

@router.delete(
        "",
        status_code=204
)
async def delete_user(
    user_dep: UserDep,
    uow: UOWDep
):
    await UsersService.delete_user(uow, user_dep['id'])

@router.patch("")
async def edit_user(
    user_dep: UserDep,
    user: UserEditDTO,
    uow: UOWDep
):
    await UsersService.edit_user(uow, user_dep['id'], user)
    return {"user_id": user_dep['id']}