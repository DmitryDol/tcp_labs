import math

from api.dependencies.pagination_dependency import PaginationParams
from dto import (
    BackgroundDTO,
    PaginatedRoadmapsDTO,
    SimplifiedRoadmapDTO,
    UserRoadmapAddDTO,
    UserRoadmapDTO,
    UserRoadmapEditDTO,
)
from utils.unitofwork import IUnitOfWork


class UserRoadmapsService:
    @staticmethod
    async def link_user_to_roadmap(
        uow: IUnitOfWork, roadmap_id: int, user_id: int
    ) -> UserRoadmapAddDTO:
        async with uow:
            user_roadmap_id = await uow.user_roadmaps.add_one(
                {"roadmap_id": roadmap_id, "user_id": user_id}
            )
            await uow.commit()
            return UserRoadmapAddDTO.model_validate(user_roadmap_id, from_attributes=True)

    @staticmethod
    async def change_background(
        uow: IUnitOfWork, roadmap_id: int, user_id: int, background: UserRoadmapEditDTO
    ):
        background_dict = background.model_dump(exclude_unset=True)
        async with uow:
            await uow.user_roadmaps.edit_one(
                id_or_filter={"roadmap_id": roadmap_id, "user_id": user_id},
                data=background_dict,
            )
            await uow.commit()

    @staticmethod
    async def get_user_roadmaps(uow: IUnitOfWork, user_id: int):
        async with uow:
            user_roadmaps: list[UserRoadmapDTO] = await uow.user_roadmaps.find_all(
                {"user_id": user_id}
            )
            roadmaps = [roadmap.roadmap_id for roadmap in user_roadmaps]
            return roadmaps

    @staticmethod
    async def delete_user_roadmap(uow: IUnitOfWork, user_roadmap_id: dict[str, int]):
        async with uow:
            user_roadmap = await uow.user_roadmaps.delete_one(user_roadmap_id)
            await uow.commit()
            return user_roadmap

    @staticmethod
    async def get_background(
        uow: IUnitOfWork, user_roadmap_id: dict[str, int]
    ) -> BackgroundDTO:
        async with uow:
            user_roadmap = await uow.user_roadmaps.find_one(
                user_id=user_roadmap_id["user_id"],
                roadmap_id=user_roadmap_id["roadmap_id"],
            )
            if user_roadmap is None:
                return None
            return BackgroundDTO.model_validate(user_roadmap, from_attributes=True)

    @staticmethod
    async def get_linked_roadmaps(
        uow: IUnitOfWork,
        pagination: PaginationParams,
        user_id: int,
        search: str | None = None,
        difficulty: str | None = None,
    ) -> PaginatedRoadmapsDTO:
        """
        Gets roadmaps linked to user_id with search and filtering capabilities

        Args:
            uow: Unit of Work instance
            user_id: id of the user
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty can be 'easy', 'medium' or 'hard'
            pagination: Pagination parameters

        Returns:
            PaginatedRoadmapsDTO object
        """
        async with uow:
            user_roadmaps_list = await uow.user_roadmaps.find_all({"user_id": user_id})
            roadmap_ids = [ur.roadmap_id for ur in user_roadmaps_list]

            roadmaps, total_count = await uow.user_roadmaps.find_user_roadmaps(
                roadmap_ids=roadmap_ids,
                search=search,
                difficulty=difficulty,
                pagination=pagination,
            )

            simplified_roadmaps = [
                SimplifiedRoadmapDTO.model_validate(roadmap, from_attributes=True)
                for roadmap in roadmaps
            ]

            total_pages = (
                math.ceil(total_count / pagination.limit) if pagination.limit > 0 else 0
            )

            return PaginatedRoadmapsDTO(
                roadmaps=simplified_roadmaps,
                total_pages=total_pages,
            )

    @staticmethod
    async def get_roadmaps_with_in_progress_cards(
        uow: IUnitOfWork,
        pagination: PaginationParams,
        user_id: int,
        search: str | None = None,
        difficulty: str | None = None,
    ) -> PaginatedRoadmapsDTO:
        """
        Gets roadmaps linked to user that have at least one card with 'in_progress' status

        Args:
            uow: Unit of Work instance
            user_id: id of the user
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty can be 'easy', 'medium' or 'hard'
            pagination: Pagination parameters

        Returns:
            PaginatedRoadmapsDTO object
        """
        async with uow:
            user_roadmaps_list = await uow.user_roadmaps.find_all({"user_id": user_id})
            roadmap_ids = [ur.roadmap_id for ur in user_roadmaps_list]

            (
                roadmaps,
                total_count,
            ) = await uow.user_roadmaps.find_roadmaps_with_in_progress_cards(
                roadmap_ids=roadmap_ids,
                user_id=user_id,
                search=search,
                difficulty=difficulty,
                pagination=pagination,
            )

            simplified_roadmaps = [
                SimplifiedRoadmapDTO.model_validate(roadmap, from_attributes=True)
                for roadmap in roadmaps
            ]

            total_pages = (
                math.ceil(total_count / pagination.limit) if pagination.limit > 0 else 0
            )

            return PaginatedRoadmapsDTO(
                roadmaps=simplified_roadmaps,
                total_pages=total_pages,
            )
