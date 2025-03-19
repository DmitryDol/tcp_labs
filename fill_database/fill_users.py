import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from orm_models import User
from faker import Faker
from datetime import datetime

current_year = datetime.utcnow().year
current_month = datetime.utcnow().month
fake = Faker('en_US')

async def add_users():
    async with SessionLocal() as session:
        users = []
        for _ in range(5):
            name = fake.name() 
            user = User(
                name=name, 
                login=name.lower().replace(" ", "_")+'@gmail.com',
                password_hash = fake.password(),
                created_at = datetime.utcnow(),
                avatar='standart_avatar'
            )
            users.append(user)

        session.add_all(users)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_users())
