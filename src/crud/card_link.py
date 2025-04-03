from sqlalchemy import text, insert
from database import async_session_factory, async_engine
from models import CardLink
import asyncio
from dto import CardLinkDTO


class CardLink:

    @staticmethod
    async def add_card_link(data: list[CardLink]) -> None:
        """
        Adds a list of CardLink objects to the database.
        Args:
            data (list[CardLink]): A list of CardLink objects to be added to the database.
        Returns:
            None
        """
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_card_link(card_link_id: int) -> None:
        """
        Deletes a card_link from the database by its ID.
        Args:
            card_link_id (int): The ID of the card_link to be deleted.
        Returns:
            None   
        """
        async with async_session_factory() as session:
            roadmap = await session.get(CardLink, card_link_id)
            if roadmap:
                await session.delete(roadmap)
                await session.commit()

    @staticmethod
    async def update_card_link(card_link_id: int, **params) -> None:
        """
        Updates the attributes of a user_roadmap in the database.
        Args:
            user_roadmap_id (int): The ID of the user_roadmap to update.
        Kwargs:
            **params: attributes to update and their new values.
                link_title (str): text describing the link
                link_content (str): link URL
        Returns:
            None
        """
        async with async_session_factory() as session:
            roadmap = await session.get(CardLink, card_link_id)
            if roadmap:
                for key, value in params.items():
                    setattr(roadmap, key, value)
            await session.commit()

    @staticmethod
    async def get_card_link(card_link_id: int) -> CardLinkDTO:
        """
        Returns card_link information based on the provided user_card_id.
        Args:
            card_link_id (int): The ID of the card_link to return.
        Returns:
            CardLinkDTO: A data transfer object containing the card_link's information.
        """
        async with async_session_factory() as session:
            user_roadmap = await session.get(CardLink, card_link_id)
            roadmap_dto = CardLinkDTO.model_validate(user_roadmap, from_attributes=True)
            return roadmap_dto