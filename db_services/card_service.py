from sqlalchemy import text, insert
from src.database import async_session_factory, async_engine
from src.models import Card, Roadmap
import asyncio
from src.dto import CardDTO


class CardService:

    @staticmethod
    async def add_card(data):
        async with async_session_factory() as session:
            session.add_all(data)
            await session.commit()

    @staticmethod
    async def delete_card(card_id):
        async with async_session_factory() as session:
            card = await session.get(Card, card_id)
            if card:
                await session.delete(card)
                await session.commit()

    @staticmethod
    async def update_card(card_id, **params):
        async with async_session_factory() as session:
            card = await session.get(Card, card_id)
            if card:
                for key, value in params.items():
                    setattr(card, key, value)
            await session.commit()

    @staticmethod
    async def get_card_info(card_id):
        async with async_session_factory() as session:
            card = await session.get(Card, card_id)
            if card:
                card_dto = CardDTO.model_validate(card, from_attributes=True)
                return card_dto

if __name__ == "__main__":
    # data = [
    #     Card(
    #         title="Введение в машинное обучение", 
    #         description="Основные концепции машинного обучения, типы алгоритмов.",
    #         roadmap_id=3,
    #         order_position=1
    #         ),
    #     Card(
    #         title="Линейная алгебра для ML", 
    #         description="Матрицы, векторы, собственные значения – ключевые темы для понимания алгоритмов.",
    #         roadmap_id=3,
    #         order_position=2
    #         ),
    #     Card(
    #         title="Градиентный спуск", 
    #         description="Как работает градиентный спуск и почему он так важен в оптимизации моделей.",
    #         roadmap_id=3,
    #         order_position=3
    #         ),
    #     Card(
    #         title="Сортировка и поиск", 
    #         description="Разбор популярных алгоритмов сортировки (quick sort, merge sort) и поиска.",
    #         roadmap_id=1,
    #         order_position=1
    #         ),
    #     Card(
    #         title="Деревья и графы", 
    #         description="Бинарные деревья, обходы в глубину и ширину, алгоритмы кратчайшего пути.",
    #         roadmap_id=1,
    #         order_position=2
    #         ),
    #     Card(
    #         title="Динамическое программирование", 
    #         description="Основные принципы динамического программирования и примеры решений классических задач.",
    #         roadmap_id=1,
    #         order_position=3
    #         )
    # ]
    # asyncio.run(CardService.add_card(data))
    
    print(asyncio.run(CardService.get_card_info(19)))