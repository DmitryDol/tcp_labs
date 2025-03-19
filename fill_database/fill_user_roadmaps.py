import asyncio
import random
from sqlalchemy.future import select
from database import SessionLocal
from orm_models import UserRoadmap, User, Roadmap

async def add_user_roadmaps():
    async with SessionLocal() as session:
        users = await session.execute(select(User.user_id))
        users = [row[0] for row in users.fetchall()] 

        roadmaps = await session.execute(select(Roadmap.roadmap_id))
        roadmaps = [row[0] for row in roadmaps.fetchall()]  


        user_roadmaps = [
            UserRoadmap(
                user_id = random.choice(users),
                roadmap_id = random.choice(roadmaps),
                role = random.choice(list(UserRoadmap.RoleEnum)),
                background = "standart_background"
            )
            for _ in range(3)
        ]

        session.add_all(user_roadmaps)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_user_roadmaps())
