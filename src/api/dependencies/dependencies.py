from typing import Annotated

from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from redis.asyncio import Redis
from starlette import status

from api.security import oauth2_bearer
from config import settings
from utils.unitofwork import IUnitOfWork, UnitOfWork


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        login: str | None = payload.get("sub")
        user_id: int | None = payload.get("id")
        user_name: str | None = payload.get("username")

        if login is None or user_id is None or user_name is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )

        return {"login": login, "id": user_id, "username": user_name}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


async def get_redis_client(request: Request):
    redis_client = request.app.state.redis_client
    if not redis_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Redis client not avialible.",
        )
    return redis_client


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
UserDep = Annotated[dict, Depends(get_current_user)]
RedisDep = Annotated[Redis, Depends(get_redis_client)]
