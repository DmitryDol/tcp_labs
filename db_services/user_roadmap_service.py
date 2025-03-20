from sqlalchemy import text, insert
from src.database import async_session_factory, async_engine
from src.models import UserRoadmap
import asyncio
from src.dto import UserRoadmapDTO


class UserRoadmapService:

    @staticmethod
    async def add_user_roadmap(data):
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_user_roadmap(user_roadmap_id):
        async with async_session_factory() as session:
            roadmap = await session.get(UserRoadmap, user_roadmap_id)
            if roadmap:
                await session.delete(roadmap)
                await session.commit()

    @staticmethod
    async def update_user_roadmap(user_roadmap_id, **params):
        async with async_session_factory() as session:
            roadmap = await session.get(UserRoadmap, user_roadmap_id)
            if roadmap:
                for key, value in params.items():
                    setattr(roadmap, key, value)
            await session.commit()

    @staticmethod
    async def get_user_roadmap_info(user_roadmap_id):
         async with async_session_factory() as session:
            user_roadmap = await session.get(UserRoadmap, user_roadmap_id)
            roadmap_dto = UserRoadmapDTO.model_validate(user_roadmap, from_attributes=True)
            return roadmap_dto


if __name__ == "__main__":
    # data = [
    #     UserRoadmap(
    #         user_id=1,
    #         roadmap_id=1
    #     ),
    #     UserRoadmap(
    #         user_id=2,
    #         roadmap_id=2
    #     ) 
    # ]
    # asyncio.run(UserRoadmapService.add_user_roadmap(data))

    # asyncio.run(UserRoadmapService.delete_user_roadmap(2))
    # asyncio.run(UserRoadmapService.update_user_roadmap((1, 1), background="smth.jpg"))

    # # проверка получения информации 
    roadmap = asyncio.run(UserRoadmapService.get_user_roadmap_info((1, 1)))
    print(roadmap)