from models import CardLink
from utils.repository import SQLAlchemyRepository

class CardLinkRepository(SQLAlchemyRepository):
    model = CardLink