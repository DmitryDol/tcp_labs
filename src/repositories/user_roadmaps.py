from src.models import UserRoadmap
from src.utils.repository import SQLAlchemyRepository

class UserRoadmapRepository(SQLAlchemyRepository):
    model = UserRoadmap