from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from config import settings
from utils.unitofwork import IUnitOfWork, UnitOfWork


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: Optional[str]= payload.get('sub')
        user_id: Optional[int]= payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user."
            )
        
        return {'username': username, 'id': user_id}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user."
        )

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
UserDep = Annotated[dict, Depends(get_current_user)]
