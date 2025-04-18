import datetime
from typing import Annotated, Any, Dict, Optional
from dto import UserAddDTO, UserEditDTO
from utils.unitofwork import IUnitOfWork
from utils.utils import hash_password, verify_password


class TokensService:
    @staticmethod
    async def is_token_revoked(uow: IUnitOfWork, jti: str) -> bool:
        async with uow:
            token = await uow.tokens.find_one(token_jti=jti)
            return token is not None

    @staticmethod
    async def revoke_token(uow: IUnitOfWork, jti: str, expires_at: datetime) -> None:
        async with uow:
            await uow.tokens.add_one({"token_jti": jti, "expires_at": expires_at})
            await uow.commit()

    @staticmethod
    async def cleanup_expired_tokens(uow: IUnitOfWork) -> None:
        async with uow:
            await uow.tokens.cleanup_expired_tokens()
            uow.commit()