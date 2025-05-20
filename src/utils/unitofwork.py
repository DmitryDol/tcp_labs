from abc import ABC, abstractmethod

from database import async_session_factory
from repositories.card_links import CardLinkRepository
from repositories.cards import CardRepository
from repositories.roadmaps import RoadmapRepository
from repositories.user_cards import UserCardRepository
from repositories.user_roadmaps import UserRoadmapRepository
from repositories.users import UserRepository


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    users: type[UserRepository]
    roadmaps: type[RoadmapRepository]
    cards: type[CardRepository]
    user_cards: type[UserCardRepository]
    user_roadmaps: type[UserRoadmapRepository]
    card_links: type[CardLinkRepository]

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.roadmaps = RoadmapRepository(self.session)
        self.cards = CardRepository(self.session)
        self.user_cards = UserCardRepository(self.session)
        self.user_roadmaps = UserRoadmapRepository(self.session)
        self.card_links = CardLinkRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
