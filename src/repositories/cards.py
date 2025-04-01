from src.models import Card
from src.utils.repository import SQLAlchemyRepository

class CardRepository(SQLAlchemyRepository):
    model = Card