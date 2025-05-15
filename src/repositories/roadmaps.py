from typing import Any, List, Optional

from sqlalchemy import select
from dto import RoadmapDTO, UserRoadmapDTO
from models import Roadmap
from utils.repository import SQLAlchemyRepository

class RoadmapRepository(SQLAlchemyRepository):
    model = Roadmap

    async def find_public_roadmaps(self, search: Optional[str] = None, difficulty: Optional[str] = None, limit: Optional[int] = None) -> List[Any]:
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
        
        if limit and isinstance(limit, int) and limit > 0:
            stmt = stmt.limit(limit)

        res = await self.session.execute(stmt)
    
        results = res.scalars().all()
        if results and hasattr(results[0], 'to_read_model'):
            return [item.to_read_model() for item in results]
        return results
    
    async def find_user_roadmaps(self, roadmap_ids: List[int], search: Optional[str] = None, difficulty: Optional[str] = None, limit: Optional[int] = None) -> List[RoadmapDTO]:
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
        
        if limit and isinstance(limit, int) and limit > 0:
            stmt = stmt.limit(limit)
        
        res = await self.session.execute(stmt)
        
        results = res.scalars().all()
        if results and hasattr(results[0], 'to_read_model'):
            return [item.to_read_model() for item in results]
        return results
