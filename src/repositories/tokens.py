from datetime import datetime, UTC
from sqlalchemy import delete
from models import TokenBlacklist
from utils.repository import SQLAlchemyRepository

class TokenRepository(SQLAlchemyRepository):
    model = TokenBlacklist

    async def cleanup_expired_tokens(self) -> None:
        
        stmt = delete(self.model).where(self.model.expires_at < datetime.now(UTC))
        await self.session.execute(stmt)
        