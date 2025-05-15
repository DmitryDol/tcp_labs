from typing import Any, List, Optional

from sqlalchemy import select
from api.dependencies.pagination_dependency import PaginationParams
from dto import RoadmapDTO, UserRoadmapDTO
from models import Roadmap
from utils.repository import SQLAlchemyRepository

class RoadmapRepository(SQLAlchemyRepository):
    model = Roadmap

    async def find_public_roadmaps(self, pagination: PaginationParams, search: Optional[str] = None, difficulty: Optional[str] = None) -> List[Any]:
        """ 
        Find public roadmaps with search and filtering capabilities
        
        Args:
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty can be 'easy', 'medium' or 'hard'
            limit: Optional limit on the number of roadmaps returned
        
        Returns:
            List of the RoadmapDTO objects
        """

        stmt = select(self.model).filter(self.model.visibility == self.model.VisibilityEnum.public)
        if search:
            stmt = stmt.filter(self.model.title.ilike(f'%{search}%'))

        if difficulty:
            try:
                difficulty_enum = self.model.DifficultyEnum(difficulty)
                stmt = stmt.filter(self.model.difficulty == difficulty_enum)
            except ValueError:
                pass
        
        if pagination:
            stmt = stmt.limit(pagination.limit).offset(pagination.offset)

        res = await self.session.execute(stmt)
    
        results = res.scalars().all()
        if results and hasattr(results[0], 'to_read_model'):
            return [item.to_read_model() for item in results]
        return results
    
    
