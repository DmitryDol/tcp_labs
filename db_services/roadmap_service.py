from sqlalchemy import text, insert
from src.database import async_session_factory, async_engine
from src.models import Roadmap
import asyncio
from src.dto import RoadmapDTO

class RoadmapService:

    @staticmethod
    async def add_roadmap(data):
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_roadmap(roadmap_id):
        async with async_session_factory() as session:
            roadmap = await session.get(Roadmap, roadmap_id)
            if roadmap:
                await session.delete(roadmap)
                await session.commit()

    @staticmethod
    async def update_roadmap(roadmap_id, **params):
        async with async_session_factory() as session:
            roadmap = await session.get(Roadmap, roadmap_id)
            if roadmap:
                for key, value in params.items():
                    setattr(roadmap, key, value)
            await session.commit()

    @staticmethod
    async def get_roadmap_info(roadmap_id):
         async with async_session_factory() as session:
            roadmap = await session.get(Roadmap, roadmap_id)
            roadmap_dto = RoadmapDTO.model_validate(roadmap, from_attributes=True)
            return roadmap_dto


if __name__ == "__main__":
    # data = [
    #     Roadmap(
    #     title="Алгоритмы и структуры данных",
    #     owner_id=1,
    #     description="Руководство по изучению базовых и продвинутых алгоритмов для эффективного программирования",
    #     difficulty= Roadmap.DifficultyEnum.medium,
    #     edit_permission=Roadmap.EditPermissionEnum.can_edit,
    #     visibility=Roadmap.VisibilityEnum.public
    # ),
    #     Roadmap(
    #     title="Машинное обучение с нуля",
    #     owner_id = 2,
    #     description="Последовательный план изучения основ машинного обучения: от базовых концепций до реализации моделей.",
    #     difficulty=Roadmap.DifficultyEnum.hard,
    #     edit_permission=Roadmap.EditPermissionEnum.view_only,
    #     visibility=Roadmap.VisibilityEnum.link_only
    # ) 
    # ]
    # asyncio.run(RoadmapService.add_roadmap(data))

    # asyncio.run(RoadmapService.delete_roadmap(2))
    # asyncio.run(RoadmapService.update_roadmap(3, visibility=Roadmap.VisibilityEnum.public))

    # проверка получения информации 
    roadmap = asyncio.run(RoadmapService.get_roadmap_info(1))
    print(roadmap)