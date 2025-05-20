import logging
import math

from api.dependencies.pagination_dependency import PaginationParams
from dto import (
    PaginatedRoadmapsDTO,
    RoadmapAddDTO,
    RoadmapDTO,
    RoadmapEditDTO,
    RoadmapExtendedDTO,
    SimplifiedRoadmapDTO,
)
from services.cards import CardsService
from utils.unitofwork import IUnitOfWork

logger = logging.getLogger(__name__)


class RoadmapsService:
    @staticmethod
    async def add_roadmap(uow: IUnitOfWork, roadmap: RoadmapAddDTO):
        roadmap_dict = roadmap.model_dump()
        async with uow:
            roadmap_id = await uow.roadmaps.add_one(roadmap_dict)
            await uow.commit()
            owner_id = (await RoadmapsService.get_roadmap(uow, roadmap_id)).owner_id
            return roadmap_id, owner_id

    @staticmethod
    async def edit_roadmap(uow: IUnitOfWork, roadmap_id: int, roadmap: RoadmapEditDTO):
        roadmap_dict = roadmap.model_dump(exclude_unset=True)
        async with uow:
            await uow.roadmaps.edit_one(roadmap_id, roadmap_dict)
            await uow.commit()

    @staticmethod
    async def get_roadmap(uow: IUnitOfWork, roadmap_id: int) -> RoadmapDTO | None:
        async with uow:
            roadmaps = await uow.roadmaps.find_one(id=roadmap_id)
            return roadmaps

    @staticmethod
    async def get_roadmaps(uow: IUnitOfWork, roadmap_ids: list[int]):
        async with uow:
            roadmaps = await uow.roadmaps.find_all(id=roadmap_ids)
            return roadmaps

    @staticmethod
    async def get_roadmap_extended(uow: IUnitOfWork, roadmap_id: int):
        async with uow:
            roadmap = await uow.roadmaps.find_one(id=roadmap_id)

            if roadmap is None:
                return None

            roadmap_dict = roadmap.model_dump()
            cards = await uow.cards.find_all({"roadmap_id": roadmap_id})
            roadmap_dict["cards"] = []
            for card in cards:
                roadmap_dict["cards"].append(
                    await CardsService.get_card_extended(uow, card.id)
                )
            logger.debug("\n\n\n", roadmap_dict, "\n\n\n")
            extended_roadmap = RoadmapExtendedDTO.model_validate(
                roadmap_dict, from_attributes=True
            )
            return extended_roadmap

    @staticmethod
    async def get_public_roadmaps(
        uow: IUnitOfWork,
        pagination: PaginationParams,
        search: str | None = None,
        difficulty: str | None = None,
    ) -> PaginatedRoadmapsDTO:
        """
        Gets public roadmaps with search and filtering capabilities

        Args:
            uow: Unit of Work instance
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty can be 'easy', 'medium' or 'hard'
            pagination: Pagination parameters

        Returns:
            PaginatedRoadmapsDTO object
        """
        async with uow:
            roadmaps, total_count = await uow.roadmaps.find_public_roadmaps(
                search=search, difficulty=difficulty, pagination=pagination
            )
            simplified_roadmaps = [
                SimplifiedRoadmapDTO.model_validate(roadmap, from_attributes=True)
                for roadmap in roadmaps
            ]

            total_pages = (
                math.ceil(total_count / pagination.limit) if pagination.limit > 0 else 0
            )

            return PaginatedRoadmapsDTO(
                roadmaps=simplified_roadmaps, total_pages=total_pages
            )

    @staticmethod
    async def delete_roadmap(uow: IUnitOfWork, roadmap_id: int):
        async with uow:
            roadmap = await uow.roadmaps.delete_one(roadmap_id)
            await uow.commit()
            return roadmap
