from src.database import async_session_factory
from src.models import UserRoadmap
import asyncio
from src.dto import UserRoadmapDTO


class UserRoadmap:

    @staticmethod
    async def add_user_roadmap(data: list[UserRoadmap]) -> None:
        """
        Adds a list of UserRoadmap objects to the database.
        Args:
            data (list[UserRoadmap]): A list of UserRoadmap objects to be added to the database.
        Returns:
            None
        """
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_user_roadmap(user_roadmap_id: int) -> None:
        """
        Deletes a user_roadmap from the database by its ID.
        Args:
            user_roadmap_id (int): The ID of the user_roadmap to be deleted.
        Returns:
            None   
        """
        async with async_session_factory() as session:
            roadmap = await session.get(UserRoadmap, user_roadmap_id)
            if roadmap:
                await session.delete(roadmap)
                await session.commit()

    @staticmethod
    async def update_user_roadmap(user_roadmap_id: int, **params) -> None:
        """
        Updates the attributes of a user_roadmap in the database.
        Args:
            user_roadmap_id (int): The ID of the user_roadmap to update.
        Kwargs:
            **params: attributes to update and their new values.
                background (str): The backgrount image name, that stored in the MinIO
        Returns:
            None
        """
        async with async_session_factory() as session:
            roadmap = await session.get(UserRoadmap, user_roadmap_id)
            if roadmap:
                for key, value in params.items():
                    setattr(roadmap, key, value)
            await session.commit()

    @staticmethod
    async def get_user_roadmap_info(user_roadmap_id: int) -> UserRoadmapDTO:
        """
        Returns user_roadmap information based on the provided user_card_id.
        Args:
            user_roadmap_id (int): The ID of the user_roadmap to return.
        Returns:
            UserRoadmapDTO: A data transfer object containing the user_roadmap's information.
        """
        async with async_session_factory() as session:
            user_roadmap = await session.get(UserRoadmap, user_roadmap_id)
            roadmap_dto = UserRoadmapDTO.model_validate(user_roadmap, from_attributes=True)
            return roadmap_dto