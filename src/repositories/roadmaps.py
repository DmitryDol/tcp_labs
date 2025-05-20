from typing import Any

from sqlalchemy import func, select

from api.dependencies.pagination_dependency import PaginationParams
from models import Roadmap
from utils.repository import SQLAlchemyRepository


class RoadmapRepository(SQLAlchemyRepository):
    model = Roadmap

    async def find_public_roadmaps(
        self,
        pagination: PaginationParams,
        search: str | None = None,
        difficulty: str | None = None,
    ) -> tuple[list[Any], int]:
        """
        Find public roadmaps with search and filtering capabilities

        Args:
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty can be 'easy', 'medium' or 'hard'
            pagination: Pagination parameters

        Returns:
            Tuple containing a list of RoadmapDTO objects and the total count.
        """

        stmt = select(self.model).filter(
            self.model.visibility == self.model.VisibilityEnum.public
        )
        if search:
            stmt = stmt.filter(self.model.title.ilike(f"%{search}%"))

        if difficulty:
            try:
                difficulty_enum = self.model.DifficultyEnum(difficulty)
                stmt = stmt.filter(self.model.difficulty == difficulty_enum)
            except ValueError:
                pass

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_count = await self.session.scalar(count_stmt)

        if pagination:
            stmt = stmt.limit(pagination.limit).offset(
                (pagination.page - 1) * pagination.limit
            )

        res = await self.session.execute(stmt)

        results = res.scalars().all()
        if results and hasattr(results[0], "to_read_model"):
            return [item.to_read_model() for item in results], total_count

        return results, total_count
