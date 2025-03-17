import asyncio
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from orm_models import UserCard, User, UserRoadmap, RoadmapCard

async def add_user_cards():
    async with SessionLocal() as session:
        users = await session.execute(select(User.user_id))
        users = [row[0] for row in users.fetchall()]

        user_cards = [] 
        for user_id in users:
            result = await session.execute(
                select(RoadmapCard.card_id)
                .join(UserRoadmap, UserRoadmap.roadmap_id == RoadmapCard.roadmap_id)
                .where(UserRoadmap.user_id == user_id)
            )
            cards = [row[0] for row in result.fetchall()]

            for card_id in cards:
                user_cards.append(
                    UserCard(
                        user_id=user_id,
                        card_id=card_id,
                        status=random.choice(list(UserCard.StatusEnum))  
                    )
                )

        session.add_all(user_cards)
        await session.commit()
           
if __name__ == "__main__":
    asyncio.run(add_user_cards())
