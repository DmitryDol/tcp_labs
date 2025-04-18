from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm#, OAuth2PasswordBearer
from config import settings
from dto import TokenDTO, UserAddDTO, UserEditDTO
from api.dependencies import UOWDep
from services.users import UsersService
from starlette import status

from datetime import timedelta

from utils.utils import create_access_token


#oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: UOWDep
):
    user = await UsersService.authenticate_user(uow, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user."
        )
    token = create_access_token(user.id, user.login, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}