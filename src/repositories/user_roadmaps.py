from models import UserRoadmap
from utils.repository import SQLAlchemyRepository

class UserRoadmapRepository(SQLAlchemyRepository):
    model = UserRoadmap