import asyncio
from sqlalchemy.future import select
from database import SessionLocal
from orm_models import RoadmapCard, Roadmap, Card 

async def add_roadmap_cards():
    async with SessionLocal() as session:
        roadmaps = await session.execute(select(Roadmap.roadmap_id))
        roadmaps = [row[0] for row in roadmaps.fetchall()] 

        cards = await session.execute(select(Card.card_id))
        cards = [row[0] for row in cards.fetchall()]  

        user_cards = []
        for i in range(len(cards)):
            rc = RoadmapCard(
                roadmap_id = 2,
                card_id = cards[i],
                order_position = i+1
            )
            user_cards.append(rc)
        
        session.add_all(user_cards)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_roadmap_cards())
