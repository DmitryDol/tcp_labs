from abc import ABC, abstractmethod
from typing import Type

from src.database import async_session_factory
from repositories.users import UserRepository
from repositories.roadmaps import RoadmapRepository
from repositories.cards import CardRepository
from repositories.user_cards import UserCardRepository
from repositories.user_roadmaps import UserRoadmapRepository
from repositories.card_links import CardLinkRepository

# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    users: Type[UserRepository]
    roadmaps: Type[RoadmapRepository]
    card: Type[CardRepository]
    user_card: Type[UserCardRepository]
    user_roadmap: Type[UserRoadmapRepository]
    card_link: Type[CardLinkRepository]
    
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.roadmaps = RoadmapRepository(self.session)
        self.card = CardRepository(self.session)
        self.user_card = UserCardRepository(self.session)
        self.user_roadmap = UserRoadmapRepository(self.session)
        self.card_link = CardLinkRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
