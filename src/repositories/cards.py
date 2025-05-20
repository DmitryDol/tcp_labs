from models import Card
from utils.repository import SQLAlchemyRepository


class CardRepository(SQLAlchemyRepository):
    model = Card
