from sqlalchemy import select

from dto import UserAuthDTO
from models import User
from utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_auth_info(self, login: str) -> UserAuthDTO | None:
        """
        Find a single record by filter criteria

        Args:
            login: Filter conditions

        Returns:
            Single model instance or None if not found
        """
        stmt = select(self.model).filter_by(login=login)
        res = await self.session.execute(stmt)
        result = res.scalar_one_or_none()
        if result is None:
            return None
        return UserAuthDTO.model_validate(result, from_attributes=True)
