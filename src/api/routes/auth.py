from typing import Annotated, Optional
from fastapi import APIRouter, Cookie, Depends, HTTPException, Path, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from config import settings
from dto import TokenDTO, UserAddDTO, UserEditDTO
from api.dependencies import UOWDep
from services.tokens import TokensService
from services.users import UsersService
from starlette import status

from datetime import UTC, datetime, timedelta

from utils.utils import create_access_token


#oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

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
    user_id = await UsersService.add_user(uow, user)
    return {"user_id": user_id}


@router.post(
    "/token",
    response_model=TokenDTO
)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: UOWDep
):
    user = await UsersService.authenticate_user(uow, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user."
        )
    access_token = create_access_token(user.id, user.login, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    refresh_token = create_access_token(user.id, user.login, timedelta(days=7))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post(
    '/refresh',
    response_model=TokenDTO
)
async def refresh_token(
    response: Response,
    uow: UOWDep,
    refresh_token: Optional[str] = Cookie(None)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )
    
    payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload.get("id")
    user_login = payload.get('sub')
    jti = payload.get("jti")

    if user_id is None or jti is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    if await TokensService.is_token_revoked(uow, jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(user_id, user_login, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_access_token(user_id, user_login, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    await TokensService.revoke_token(uow, jti, datetime.now(UTC))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/logout')
async def logout(
    response: Response,
    uow: UOWDep,
    access_token: Optional[str] = Cookie(None),
    refresh_token: Optional[str] = Cookie(None)
):
    if access_token:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        jti = payload.get('jti')
        exp = payload.get('exp')
        if jti and exp:
            expires_at = datetime.fromtimestamp(exp)
            await TokensService.revoke_token(uow, jti, expires_at)

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    
    return {"detail": "Successfully logged out"}