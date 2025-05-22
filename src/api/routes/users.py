from fastapi import APIRouter, Cookie, Response

from api.dependencies.dependencies import RedisDep, UOWDep, UserDep
from dto import AvatarDTO, UserDTO, UserEditDTO
from services.tokens import TokensService
from services.users import UsersService
from utils.utils import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=UserDTO)
async def get_user_info(user_dep: UserDep, uow: UOWDep):
    user = await UsersService.get_user(uow, id=user_dep["id"])
    return user


@router.delete("", status_code=204)
async def delete_user(
    user_dep: UserDep,
    uow: UOWDep,
    redis_dep: RedisDep,
    response: Response,
    access_token: str | None = Cookie(None),
    refresh_token: str | None = Cookie(None),
):
    await UsersService.delete_user(uow, user_dep["id"])

    if access_token:
        jti, expires_at = TokensService.prepare_token_for_revocation(access_token)
        if jti and expires_at:
            await TokensService.revoke_token(jti, expires_at, redis_dep)

    if refresh_token:
        jti, expires_at = TokensService.prepare_token_for_revocation(refresh_token)
        if jti and expires_at:
            await TokensService.revoke_token(jti, expires_at, redis_dep)

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"detail": "Successfully deleted"}


@router.patch("")
async def edit_user(user_dep: UserDep, user: UserEditDTO, uow: UOWDep):
    if user.password_hash is not None:
        user.password_hash = hash_password(user.password_hash)
    await UsersService.edit_user(uow, user_dep["id"], user)
    user_data = await UsersService.get_user(uow, id=user_dep["id"])
    return {
        "user_id": user_dep["id"],
        "login": user_data.login,
        "username": user_data.name,
    }


@router.delete("/avatar")
async def delete_user_avatar(user_dep: UserDep, uow: UOWDep):
    await UsersService.delete_avatar(uow, user_dep["id"])


@router.put("/avatar")
async def change_user_avatar(user_dep: UserDep, avatar: AvatarDTO, uow: UOWDep):
    await UsersService.edit_avatar(uow, avatar, user_dep["id"])
    return avatar


@router.get("/avatar")
async def get_user_avatar(user_dep: UserDep, uow: UOWDep):
    return await UsersService.get_avatar(uow, user_dep["id"])
