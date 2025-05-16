from typing import List, Optional

from sqlalchemy import select
from api.dependencies.pagination_dependency import PaginationParams
from dto import RoadmapDTO
from models import UserRoadmap
from utils.repository import SQLAlchemyRepository

class UserRoadmapRepository(SQLAlchemyRepository):
    model = UserRoadmap

    async def find_user_roadmaps(
            self, 
            pagination: PaginationParams, 
            roadmap_ids: List[int], 
            search: Optional[str] = None, 
            difficulty: Optional[str] = None
    ) -> List[RoadmapDTO]:
        """
        Find roadmaps linked to user with search and filtering capabilities
        
        Args:
            user_roadmaps_list: List of UserRoadmapDTO objects containing roadmap_id fields
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty can be 'easy', 'medium' or 'hard'
            limit: Optional limit on the number of roadmaps returned
        
        Returns:
            List of the RoadmapDTO objects
        """
        
        if not roadmap_ids:
            return []
        
        stmt = select(self.model).filter(self.model.id.in_(roadmap_ids))
        
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