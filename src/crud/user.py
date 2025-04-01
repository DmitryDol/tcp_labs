from sqlalchemy import insert, select
from src.database import async_session_factory
from src.models import User
import asyncio
from faker import Faker
from src.dto import UsersDTO


class User:

    @staticmethod
    async def add_user(user: User) -> None:
        """
        Adds a list of User objects to the database.
        Args:
            user: A User object to be added to the database.
        Returns:
            None
        """
        async with async_session_factory() as session:
            stmt = insert(User).values(**user)
            res = await session.execute(stmt)
            await session.commit()
            return res

    @staticmethod
    async def add_users(data: list[User]) -> None:
        """
        Adds a list of User objects to the database.
        Args:
            data (list[User]): A list of User objects to be added to the database.
        Returns:
            None
        """
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_user(user_id: int) -> None:
        """
        Deletes a user from the database by their user ID.
        Args:
            user_id (int): The ID of the user to be deleted.
        Returns:
            None   
        """
        async with async_session_factory() as session:
            user = await session.get(User, user_id)
            if user: 
                await session.delete(user)
                await session.commit()

    @staticmethod
    async def update_user(user_id: int, **params) -> None:
        """
        Updates the attributes of a user in the database.
        Args:
            user_id (int): The ID of the user to update.
            **params: attributes to update and their new values.
                name (str): The name of the user.
                login (str): The user's login.
                password_hash (str): The user's password hash.
                avatar (str): The user's avatar.
        Returns:
            None
        """
        async with async_session_factory() as session:
            user = await session.get(User, user_id)
            if user:
                for key, value in params.items():
                    setattr(user, key, value)
            await session.commit() 

    @staticmethod
    async def get_user_info(user_id: int) -> UsersDTO:
        """
        Returns user information based on the provided user ID.
        Args:
            user_id (int): The ID of the user to return.
        Returns:
            UsersDTO: A data transfer object containing the user's information.
        """
        async with async_session_factory() as session:
            user = await session.get(User, user_id)
            user_dto = UsersDTO.model_validate(user, from_attributes=True)
            return user_dto
        
    @staticmethod
    async def get_user_info_by_login(login: str) -> UsersDTO | None:
        async with async_session_factory() as session:
            stmt = select(User).where(User.login == login)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user is None:
                return None
            
            user_dto = UsersDTO.model_validate(user, from_attributes=True)
            return user_dto