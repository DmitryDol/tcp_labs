from database import async_session_factory
from dto import UserCardDTO
from models import UserCard


class UserCard:
    @staticmethod
    async def add_user_card(data: list[UserCard]) -> None:
        """
        Adds a list of UserCard objects to the database.
        Args:
            data (list[UserCard]): A list of UserCard objects to be added to the database.
        Returns:
            None
        """
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_user_card(user_card_id: int) -> None:
        """
        Deletes a user_card from the database by its ID.
        Args:
            user_card_id (int): The ID of the user_card to be deleted.
        Returns:
            None
        """
        async with async_session_factory() as session:
            user_card = await session.get(UserCard, user_card_id)
            if user_card:
                await session.delete(user_card)
                await session.commit()

    @staticmethod
    async def update_user_card(user_card_id: int, **params) -> None:
        """
        Updates the attributes of a user_card in the database.
        Args:
            user_card_id (int): The ID of the user_card to update.
        Kwargs:
            **params: attributes to update and their new values.
                status (UserCard.StatusEnum): The card status. Can be "in_progres", "done", "to_do"
        Returns:
            None
        """
        async with async_session_factory() as session:
            user_card = await session.get(UserCard, user_card_id)
            if user_card:
                for key, value in params.items():
                    setattr(user_card, key, value)
            await session.commit()

    @staticmethod
    async def get_user_card_info(user_card_id: int) -> UserCardDTO:
        """
        Returns user_card information based on the provided user_card_id.
        Args:
            user_card_id (int): The ID of the user_card to return.
        Returns:
            UserCardDTO: A data transfer object containing the user_cards's information.
        """
        async with async_session_factory() as session:
            user_card = await session.get(UserCard, user_card_id)
            roadmap_dto = UserCardDTO.model_validate(user_card, from_attributes=True)
            return roadmap_dto
