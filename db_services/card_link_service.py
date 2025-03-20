from sqlalchemy import text, insert
from src.database import async_session_factory, async_engine
from src.models import CardLink
import asyncio
from src.dto import CardLinkDTO


class CardLinkService:

    @staticmethod
    async def add_card_link(data):
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_card_link(card_link_id):
        async with async_session_factory() as session:
            roadmap = await session.get(CardLink, card_link_id)
            if roadmap:
                await session.delete(roadmap)
                await session.commit()

    @staticmethod
    async def update_card_link(card_link_id, **params):
        async with async_session_factory() as session:
            roadmap = await session.get(CardLink, card_link_id)
            if roadmap:
                for key, value in params.items():
                    setattr(roadmap, key, value)
            await session.commit()

    @staticmethod
    async def get_card_link(card_link_id):
         async with async_session_factory() as session:
            user_roadmap = await session.get(CardLink, card_link_id)
            roadmap_dto = CardLinkDTO.model_validate(user_roadmap, from_attributes=True)
            return roadmap_dto


if __name__ == "__main__":
    # data = [
    #     CardLink(
    #         card_id=1,
    #         link_title='Курс на Stepik "Введение в Data Science и машинное обучение"',
    #         link_content=r'https://stepik.org/course/4852'
    #     ),
    #     CardLink(
    #         card_id=3,
    #         link_title='Градиентный спуск простыми словами',
    #         link_content=r'https://habr.com/ru/articles/716380/'
    #     ),
    #     CardLink(
    #         card_id=4,
    #         link_title='Это база. Алгоритмы сортировки для начинающих / Хабр',
    #         link_content=r'https://habr.com/ru/companies/selectel/articles/851206/'
    #     ),
    #     CardLink(
    #         card_id=5,
    #         link_title='Алгоритмы на деревьях',
    #         link_content=r'https://neerc.ifmo.ru/wiki/index.php?title=%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D1%8B_%D0%BD%D0%B0_%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D1%8F%D1%85'
    #     ),
    #     CardLink(
    #         card_id=5,
    #         link_title='Сортировка декартовым деревом / Хабр',
    #         link_content=r'https://habr.com/ru/companies/edison/articles/505744/'
    #     ),
        
    # ]
    # asyncio.run(CardLinkService.add_card_link(data))

    # asyncio.run(CardLinkService.delete_card_link(2))
    # asyncio.run(CardLinkService.update_card_link(2, link_title=r'Градиентный спуск простыми словами / Хабр'))

    # # проверка получения информации 
    roadmap = asyncio.run(CardLinkService.get_card_link(1))
    print(roadmap)