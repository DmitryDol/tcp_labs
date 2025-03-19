from sqlalchemy import text, insert
from src.database import async_session_factory, async_engine
from src.models import User
import asyncio
from faker import Faker
from src.dto import UsersDTO

async def add_user(data):
    async with async_session_factory() as session:
        session.add(data)
        await session.commit()

async def delete_user(user_id):
    async with async_session_factory() as session:
        user = await session.get(User, user_id)
        if user: 
            await session.delete(user)
            await session.commit()

async def update_user(user_id, name=None, login=None, password_hash=None, avatar = None):
    async with async_session_factory() as session:
        user = await session.get(User, user_id)
        if user:
            if name:
                user.name = name
            if login:
                user.login = login
            if password_hash:
                user.password_hash = password_hash
            if avatar:
                user.avatar = avatar
        await session.commit() 

async def get_user_info(user_id):
    async with async_session_factory() as session:
        user = await session.get(User, user_id)
        user_dto = UsersDTO.model_validate(user, from_attributes=True)
        return user_dto



if __name__ == "__main__":

    # Пример с добавлением
    # fake = Faker('en_US')
    # for _ in range(5):
    #     name = fake.name() 
    #     user = User(
    #         name=name, 
    #         login=name.lower().replace(" ", "_")+'@gmail.com',
    #         password_hash = fake.password(),
    #     )
    #     asyncio.run(add_user(user))

    # Пример с удалением
    # asyncio.run(delete_user(5))

    # Получение информации о пользователе DTO
    print(asyncio.run(get_user_info(3)))