from typing import Annotated, Optional
from redis.asyncio import Redis
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from starlette import status

from config import settings
from utils.unitofwork import IUnitOfWork, UnitOfWork
from api.security import oauth2_bearer


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        login: Optional[str] = payload.get('sub')
        user_id: Optional[int] = payload.get('id')
        user_name: Optional[str] = payload.get('username')

        if login is None or user_id is None or user_name is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user."
            )
        
        return {'login': login, 'id': user_id, 'username': user_name}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user."
        )
    
async def get_redis_client(request: Request):
    redis_client = request.app.state.redis_client
    if not redis_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Redis client not avialible.'
        )
    return redis_client


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
UserDep = Annotated[dict, Depends(get_current_user)]
RedisDep = Annotated[Redis, Depends(get_redis_client)]