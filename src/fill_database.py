from src.crud import *
from src.models import *
import asyncio
from faker import Faker

async def main():
    
    fake = Faker('en_US')
    data = []
    for _ in range(5):
        name = fake.name() 
        user = User(
            name=name, 
            login=name.lower().replace(" ", "_")+'@gmail.com',
            password_hash = fake.password(),
        )
        data.append(user)
    await User.add_user(data)
    data = [
        Roadmap(
        title="Алгоритмы и структуры данных",
        owner_id=1,
        description="Руководство по изучению базовых и продвинутых алгоритмов для эффективного программирования",
        difficulty= Roadmap.DifficultyEnum.medium,
        edit_permission=Roadmap.EditPermissionEnum.can_edit,
        visibility=Roadmap.VisibilityEnum.public
    ),
        Roadmap(
        title="Машинное обучение с нуля",
        owner_id = 2,
        description="Последовательный план изучения основ машинного обучения: от базовых концепций до реализации моделей.",
        difficulty=Roadmap.DifficultyEnum.hard,
        edit_permission=Roadmap.EditPermissionEnum.view_only,
        visibility=Roadmap.VisibilityEnum.link_only
    ) 
    ]
    await Roadmap.add_roadmap(data)

    data = [
        Card(
            title="Введение в машинное обучение", 
            description="Основные концепции машинного обучения, типы алгоритмов.",
            roadmap_id=2,
            order_position=1
            ),
        Card(
            title="Линейная алгебра для ML", 
            description="Матрицы, векторы, собственные значения – ключевые темы для понимания алгоритмов.",
            roadmap_id=2,
            order_position=2
            ),
        Card(
            title="Градиентный спуск", 
            description="Как работает градиентный спуск и почему он так важен в оптимизации моделей.",
            roadmap_id=2,
            order_position=3
            ),
        Card(
            title="Сортировка и поиск", 
            description="Разбор популярных алгоритмов сортировки (quick sort, merge sort) и поиска.",
            roadmap_id=1,
            order_position=1
            ),
        Card(
            title="Деревья и графы", 
            description="Бинарные деревья, обходы в глубину и ширину, алгоритмы кратчайшего пути.",
            roadmap_id=1,
            order_position=2
            ),
        Card(
            title="Динамическое программирование", 
            description="Основные принципы динамического программирования и примеры решений классических задач.",
            roadmap_id=1,
            order_position=3
            )
    ]
    await Card.add_card(data)

    data = [
        UserRoadmap(
            user_id=1,
            roadmap_id=1
        ),
        UserRoadmap(
            user_id=2,
            roadmap_id=2
        ) 
    ]
    await UserRoadmap.add_user_roadmap(data)

    data = [
        UserCard(
            user_id=2,
            card_id=1,
        ),
        UserCard(
            user_id=2,
            card_id=2,
        ),
        UserCard(
            user_id=2,
            card_id=3,
        ),
        UserCard(
            user_id=1,
            card_id=4,
        ),
        UserCard(
            user_id=1,
            card_id=5,
        ),
        UserCard(
            user_id=1,
            card_id=6,
        )
    ]
    await UserCard.add_user_card(data)

    data = [
        CardLink(
            card_id=1,
            link_title='Курс на Stepik "Введение в Data Science и машинное обучение"',
            link_content=r'https://stepik.org/course/4852'
        ),
        CardLink(
            card_id=3,
            link_title='Градиентный спуск простыми словами',
            link_content=r'https://habr.com/ru/articles/716380/'
        ),
        CardLink(
            card_id=4,
            link_title='Это база. Алгоритмы сортировки для начинающих / Хабр',
            link_content=r'https://habr.com/ru/companies/selectel/articles/851206/'
        ),
        CardLink(
            card_id=5,
            link_title='Алгоритмы на деревьях',
            link_content=r'https://neerc.ifmo.ru/wiki/index.php?title=%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D1%8B_%D0%BD%D0%B0_%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D1%8C%D1%8F%D1%85'
        ),
        CardLink(
            card_id=5,
            link_title='Сортировка декартовым деревом / Хабр',
            link_content=r'https://habr.com/ru/companies/edison/articles/505744/'
        ),
        
    ]
    await CardLink.add_card_link(data)

asyncio.run(main())