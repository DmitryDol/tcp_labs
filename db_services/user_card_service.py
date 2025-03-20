from sqlalchemy import text, insert
from src.database import async_session_factory, async_engine
from src.models import UserCard
import asyncio
from src.dto import UserCardDTO


class UserCardService:

    @staticmethod
    async def add_user_card(data):
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_user_card(user_card_id):
        async with async_session_factory() as session:
            user_card = await session.get(UserCard, user_card_id)
            if user_card:
                await session.delete(user_card)
                await session.commit()

    @staticmethod
    async def update_user_card(user_card_id, **params):
        async with async_session_factory() as session:
            user_card = await session.get(UserCard, user_card_id)
            if user_card:
                for key, value in params.items():
                    setattr(user_card, key, value)
            await session.commit()

    @staticmethod
    async def get_user_card_info(user_card_id):
         async with async_session_factory() as session:
            user_card = await session.get(UserCard, user_card_id)
            roadmap_dto = UserCardDTO.model_validate(user_card, from_attributes=True)
            return roadmap_dto


if __name__ == "__main__":
    # data = [
    #     UserCard(
    #         user_id=2,
    #         card_id=1,
    #     ),
    #     UserCard(
    #         user_id=2,
    #         card_id=2,
    #     ),
    #     UserCard(
    #         user_id=2,
    #         card_id=3,
    #     ),
    #     UserCard(
    #         user_id=1,
    #         card_id=4,
    #     ),
    #     UserCard(
    #         user_id=1,
    #         card_id=5,
    #     ),
    #     UserCard(
    #         user_id=1,
    #         card_id=6,
    #     )
    # ]
    # asyncio.run(UserCardService.add_user_card(data))

    # asyncio.run(UserCardService.delete_user_card((2, 1)))
    # asyncio.run(UserCardService.update_user_card((1, 4), status=UserCard.StatusEnum.in_progress))

    # проверка получения информации 
    roadmap = asyncio.run(UserCardService.get_user_card_info((1, 4)))
    print(roadmap)