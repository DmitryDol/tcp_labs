from src.models import UserCard
from src.utils.repository import SQLAlchemyRepository

class UserCardRepository(SQLAlchemyRepository):
    model = UserCard