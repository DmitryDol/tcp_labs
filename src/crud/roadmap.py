from database import async_session_factory
from models import Roadmap
import asyncio
from dto import RoadmapDTO


class Roadmap:

    @staticmethod
    async def add_roadmap(data: list[Roadmap]) -> None:
        """
        Adds a list of Roadmap objects to the database.
        Args:
            data (list[Roadmap]): A list of Roadmap objects to be added to the database.
        Returns:
            None
        """
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_roadmap(roadmap_id: int) -> None:
        """
        Deletes a roadmap from the database by its ID.
        Args:
            roadmap_id (int): The ID of the roadmap to be deleted.
        Returns:
            None   
        """
        async with async_session_factory() as session:
            roadmap = await session.get(Roadmap, roadmap_id)
            if roadmap:
                await session.delete(roadmap)
                await session.commit()

    @staticmethod
    async def update_roadmap(roadmap_id: int, **params) -> None:
        """
        Updates the attributes of a roadmap in the database.
        Args:
            roadmap_id (int): The ID of the roadmap to update.
            **params: attributes to update and their new values.
                title (str): The title of the roadmap.
                description (str): The description of the roadmap.
                difficulty (str): The difficulty of the roadmap.
                edit_permission (str): The edit permission of the roadmap.
                visibility (str): The visibility of the roadmap.
        Kwargs:
        
        Returns:
            None
        """
        async with async_session_factory() as session:
            roadmap = await session.get(Roadmap, roadmap_id)
            if roadmap:
                for key, value in params.items():
                    setattr(roadmap, key, value)
            await session.commit()

    @staticmethod
    async def get_roadmap_info(roadmap_id) -> RoadmapDTO:
         """
        Returns roadmap information based on the provided user ID.
        Args:
            roadmap_id (int): The ID of the roadmap to return.
        Returns:
            UsersDTO: A data transfer object containing the roadmap's information.
        """
         async with async_session_factory() as session:
            roadmap = await session.get(Roadmap, roadmap_id)
            roadmap_dto = RoadmapDTO.model_validate(roadmap, from_attributes=True)
            return roadmap_dto