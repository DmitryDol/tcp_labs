from sqlalchemy import func, select

from api.dependencies.pagination_dependency import PaginationParams
from dto import RoadmapDTO
from models import Card, Roadmap, UserCard, UserRoadmap
from utils.repository import SQLAlchemyRepository


class UserRoadmapRepository(SQLAlchemyRepository):
    model = UserRoadmap

    async def find_user_roadmaps(
        self,
        pagination: PaginationParams,
        roadmap_ids: list[int],
        search: str | None = None,
        difficulty: str | None = None,
    ) -> tuple[list[RoadmapDTO], int]:
        """
        Find roadmaps linked to user with search and filtering capabilities

        Args:
            roadmap_ids: List of roadmap IDs linked to the user.
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty can be 'easy', 'medium' or 'hard'
            pagination: Pagination parameters

        Returns:
            Tuple containing a list of RoadmapDTO objects and the total count.
        """

        if not roadmap_ids:
            return [], 0

        stmt = select(Roadmap).filter(Roadmap.id.in_(roadmap_ids))

        if search:
            stmt = stmt.filter(Roadmap.title.ilike(f"%{search}%"))

        if difficulty:
            try:
                difficulty_enum = Roadmap.DifficultyEnum(difficulty)
                stmt = stmt.filter(Roadmap.difficulty == difficulty_enum)
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

    async def find_roadmaps_with_in_progress_cards(
        self,
        pagination: PaginationParams,
        roadmap_ids: list[int],
        user_id: int,
        search: str | None = None,
        difficulty: str | None = None,
    ) -> tuple[list[RoadmapDTO], int]:
        """
        Find roadmaps that have at least one card with 'in_progress' status

        Args:
            roadmap_ids: List of roadmap IDs linked to the user
            user_id: ID of the user
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty
            pagination: Pagination parameters

        Returns:
            Tuple containing a list of RoadmapDTO objects and the total count
        """
        if not roadmap_ids:
            return [], 0

        # Запрос для получения роадмапов с карточками в прогрессе
        stmt = (
            select(Roadmap)
            .join(Card, Card.roadmap_id == Roadmap.id)
            .join(UserCard, UserCard.card_id == Card.id)
            .where(
                UserCard.user_id == user_id,
                UserCard.status == "in_progress",
                Roadmap.id.in_(roadmap_ids),
            )
            .distinct()
        )

        if search:
            stmt = stmt.filter(Roadmap.title.ilike(f"%{search}%"))

        if difficulty:
            try:
                difficulty_enum = Roadmap.DifficultyEnum(difficulty)
                stmt = stmt.filter(Roadmap.difficulty == difficulty_enum)
            except ValueError:
                pass

        # Подсчет общего количества записей
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_count = await self.session.scalar(count_stmt)

        # Применяем пагинацию
        if pagination:
            stmt = stmt.limit(pagination.limit).offset(
                (pagination.page - 1) * pagination.limit
            )

        res = await self.session.execute(stmt)
        results = res.scalars().all()

        if results and hasattr(results[0], "to_read_model"):
            return [item.to_read_model() for item in results], total_count

        return results, total_count
