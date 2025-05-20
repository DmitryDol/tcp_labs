import logging
from datetime import UTC, datetime

from jose import jwt
from redis.asyncio import Redis

from config import settings

logger = logging.getLogger("TokensService")


class TokensService:
    @staticmethod
    async def is_token_revoked(jti: str, redis_client: Redis):
        key = f"token:{jti}"
        token = await redis_client.get(key)
        logger.debug(f"redis: is_token_revoked: {token}")
        return token is not None

    @staticmethod
    async def revoke_token(jti: str, expires_at: datetime, redis_client: Redis):
        key = f"token:{jti}"
        remaining_time = expires_at - datetime.now(UTC)
        if remaining_time.total_seconds() > 0:
            await redis_client.setex(key, int(remaining_time.total_seconds()), 1)
            logger.debug(f"redis: revoke_token {await redis_client.get(key)}")
        else:
            logger.debug(f"token not revoked {remaining_time.total_seconds()}")

    @staticmethod
    def prepare_token_for_revocation(token: str):
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        jti = payload.get("jti")
        exp = payload.get("exp")
        if jti and exp:
            expires_at = datetime.fromtimestamp(exp, tz=UTC)
            return jti, expires_at
        return jti, exp
