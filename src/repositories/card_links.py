from src.models import CardLink
from src.utils.repository import SQLAlchemyRepository

class CardLinkRepository(SQLAlchemyRepository):
    model = CardLink