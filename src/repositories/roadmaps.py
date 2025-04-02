from src.models import Roadmap
from src.utils.repository import SQLAlchemyRepository

class RoadmapRepository(SQLAlchemyRepository):
    model = Roadmap