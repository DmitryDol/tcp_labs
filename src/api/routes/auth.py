from typing import Annotated, Optional
from fastapi import APIRouter, Cookie, Depends, HTTPException, Path, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from config import settings
from dto import LoginDTO, TokenDTO, UserAddDTO, UserAuthDTO, UserEditDTO
from api.dependencies.dependencies import RedisDep, UOWDep, UserDep
from services.tokens import TokensService
from services.users import UsersService
from starlette import status

from datetime import UTC, datetime, timedelta

from utils.utils import create_token


router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: UserAddDTO,
    uow: UOWDep
):
    already_exist = await UsersService.get_user(uow, login=user.login)
    if already_exist is not None:
        raise HTTPException(status_code=409, detail="User with this email already exist")
    user_id = await UsersService.add_user(uow, user)
    return {"user_id": user_id}


@router.post(
    "/token",
    response_model=LoginDTO
)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: UOWDep
):
    user = await UsersService.authenticate_user(uow, form_data.username, form_data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user."
        )
    access_token = create_token(user.id, user.login, user.name, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    refresh_token = create_token(user.id, user.login, user.name, timedelta(days=7))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "username": user.name, 
        "login": user.login, 
        "avatar": user.avatar
    }

@router.post(
    '/refresh',
    response_model=TokenDTO
)
async def refresh_token(
    redis_dep: RedisDep,
    response: Response,
    access_token: Optional[str] = Cookie(None),
    refresh_token: Optional[str] = Cookie(None)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )
    
    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload.get("id")
    user_name = payload.get('username')
    user_login = payload.get('sub')
    expires_at = datetime.fromtimestamp(payload.get('exp'), tz=UTC)
    jti = payload.get("jti")

    if access_token:
        access_token_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        access_token_expires_at = datetime.fromtimestamp(access_token_payload.get('exp'), tz=UTC)
        access_token_jti = access_token_payload.get("jti")

    if user_id is None or jti is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    if await TokensService.is_token_revoked(jti, redis_dep):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked"#,
            # headers={"WWW-Authenticate": "Bearer"},
        )
    
    new_access_token = create_token(user_id, user_login, user_name, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    new_refresh_token = create_token(user_id, user_login, user_name, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

    await TokensService.revoke_token(jti, expires_at, redis_dep)

    if access_token:
        await TokensService.revoke_token(access_token_jti, access_token_expires_at, redis_dep)

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post('/logout')
async def logout(
    user_dep: UserDep,
    redis_dep: RedisDep,
    response: Response,
    access_token: Optional[str] = Cookie(None),
    refresh_token: Optional[str] = Cookie(None)
):
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
    
    return {"detail": "Successfully logged out"}

@router.get('/me')
async def get_curr_user(
    user_dep: UserDep
):
    return user_dep