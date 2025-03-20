from sqlalchemy import text, insert
from src.database import async_session_factory, async_engine
from src.models import User
import asyncio
from faker import Faker
from src.dto import UsersDTO


class UserService:
    @staticmethod
    async def add_user(data):
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_user(user_id):
        async with async_session_factory() as session:
            user = await session.get(User, user_id)
            if user: 
                await session.delete(user)
                await session.commit()

    @staticmethod
    async def update_user(user_id, **params):
        async with async_session_factory() as session:
            user = await session.get(User, user_id)
            if user:
                for key, value in params.items():
                    setattr(user, key, value)
            await session.commit() 

    @staticmethod
    async def get_user_info(user_id):
        async with async_session_factory() as session:
            user = await session.get(User, user_id)
            user_dto = UsersDTO.model_validate(user, from_attributes=True)
            return user_dto



if __name__ == "__main__":

    # Пример с добавлением
    # fake = Faker('en_US')
    # data = []
    # for _ in range(5):
    #     name = fake.name() 
    #     user = User(
    #         name=name, 
    #         login=name.lower().replace(" ", "_")+'@gmail.com',
    #         password_hash = fake.password(),
    #     )
    #     data.append(user)
    #     asyncio.run(UserService.add_user(data))

    # Пример с удалением
    # asyncio.run(delete_user(5))

    # Получение информации о пользователе DTO
    # user = asyncio.run(UserService.get_user_info(3))
    # print(user)

    # Пример с обновлением
    asyncio.run(UserService.update_user(4, name="Ivan Ivanov", login="ivanov@gmail.com"))