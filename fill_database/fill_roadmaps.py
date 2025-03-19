import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import SessionLocal
from orm_models import Roadmap


async def add_roadmaps():
    async with SessionLocal() as session:
        roadmaps = [
            Roadmap(
                title="Алгоритмы и структуры данных",
                description="Руководство по изучению базовых и продвинутых алгоритмов для эффективного программирования.",
                difficulty=Roadmap.DifficultyEnum.medium
            ),
            Roadmap(
                title="Машинное обучение с нуля",
                description="Последовательный план изучения основ машинного обучения: от базовых концепций до реализации моделей.",
                difficulty=Roadmap.DifficultyEnum.hard
            )    
        ]

        session.add_all(roadmaps)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_roadmaps())