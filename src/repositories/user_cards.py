from models import UserCard
from utils.repository import SQLAlchemyRepository

class UserCardRepository(SQLAlchemyRepository):
    model = UserCard