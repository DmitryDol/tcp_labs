from database import async_session_factory
from dto import CardDTO
from models import Card


class Card:
    @staticmethod
    async def add_card(data: list[Card]) -> None:
        """
        Adds a list of Card objects to the database.
        Args:
            data (list[Card]): A list of Card objects to be added to the database.
        Returns:
            None
        """
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_card(card_id: int) -> None:
        """
        Deletes a card from the database by its ID.
        Args:
            card_id (int): The ID of the card to be deleted.
        Returns:
            None
        """
        async with async_session_factory() as session:
            card = await session.get(Card, card_id)
            if card:
                await session.delete(card)
                await session.commit()

    @staticmethod
    async def update_card(card_id: int, **params) -> None:
        """
        Updates the attributes of a card in the database.
        Args:
            card_id (int): The ID of the card to update.
            **params: attributes to update and their new values.
                title (str): The title of the card.
                description (str): The description of the card.
        Returns:
            None
        """
        async with async_session_factory() as session:
            card = await session.get(Card, card_id)
            if card:
                for key, value in params.items():
                    setattr(card, key, value)
            await session.commit()

    @staticmethod
    async def get_card_info(card_id: int) -> CardDTO:
        """
        Returns user information based on the provided card ID.
        Args:
            card_id (int): The ID of the card to return.
        Returns:
            UsersDTO: A data transfer object containing the card's information.
        """
        async with async_session_factory() as session:
            card = await session.get(Card, card_id)
            if card:
                card_dto = CardDTO.model_validate(card, from_attributes=True)
                return card_dto
