import asyncio
from sqlalchemy.future import select
from database import SessionLocal
from orm_models import CardLink, Card

async def add_card_links():
    async with SessionLocal() as session:
        cards = await session.execute(select(Card.card_id))
        cards = [row[0] for row in cards.fetchall()] 
        card_links = [
            CardLink(
                card_id=1,
                link_title="Основы машинного обучения",
                link_content="https://example.com/intro-to-ml-basics"
            ),
            CardLink(
                card_id=1,
                link_title="Виды машинного обучения",
                link_content="https://example.com/types-of-ml"
            ),
            CardLink(
                card_id=2,
                link_title="Линейная алгебра для ML",
                link_content="https://example.com/linear-algebra-for-ml"
            ),
            CardLink(
                card_id=2,
                link_title="Статистика для анализа данных",
                link_content="https://example.com/statistics-for-data"
            ),
            CardLink(
                card_id=3,
                link_title="Pandas: обработка данных",
                link_content="https://example.com/pandas-tutorial"
            ),
            CardLink(
                card_id=3,
                link_title="NumPy: основы работы",
                link_content="https://example.com/numpy-basics"
            ),
            CardLink(
                card_id=4,
                link_title="Линейная регрессия",
                link_content="https://example.com/linear-regression"
            ),
            CardLink(
                card_id=4,
                link_title="Деревья решений",
                link_content="https://example.com/decision-trees"
            )
        ]
       
        session.add_all(card_links)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_card_links())