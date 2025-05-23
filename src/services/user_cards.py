from dto import CardDTO, RoadmapDTO, UserCardAddDTO, UserCardEditDTO
from services.roadmaps import RoadmapsService
from utils.unitofwork import IUnitOfWork


class UserCardService:
    @staticmethod
    async def add_user_card(uow: IUnitOfWork, user_card: UserCardAddDTO):
        user_card_dict = user_card.model_dump()
        async with uow:
            user_card_id = await uow.user_cards.add_one(user_card_dict)
            await uow.commit()
            return user_card_id

    @staticmethod
    async def edit_user_card(
        uow: IUnitOfWork, user_card_id: dict[str, int], user_card: UserCardEditDTO
    ):
        user_card_dict = user_card.model_dump(exclude_unset=True)
        async with uow:
            await uow.user_cards.edit_one(user_card_id, user_card_dict)
            await uow.commit()

    @staticmethod
    async def get_user_cards(uow: IUnitOfWork):
        async with uow:
            user_cards = await uow.user_cards.find_all()
            return user_cards

    @staticmethod
    async def delete_user_card(uow: IUnitOfWork, user_card_id: int):
        async with uow:
            user_card = await uow.user_cards.delete_one(user_card_id)
            await uow.commit()
            return user_card

    @staticmethod
    async def delete_user_cards(uow: IUnitOfWork, user_id: int, roadmap_id: int):
        async with uow:
            card_ids: list[CardDTO] = await uow.cards.find_all({"roadmap_id": roadmap_id})
            for card_id in card_ids:
                await uow.user_cards.delete_one(
                    {"user_id": user_id, "card_id": card_id.id}
                )
            await uow.commit()
            return card_ids

    @staticmethod
    async def link_user_to_cards_in_roadmap(
        uow: IUnitOfWork, user_id: int, roadmap_id: int
    ):
        roadmap: RoadmapDTO | None = await RoadmapsService.get_roadmap(uow, roadmap_id)

        if roadmap is None:
            return None

        async with uow:
            cards: list[CardDTO] = await uow.cards.find_all({"roadmap_id": roadmap.id})

            if not cards:
                return None

            card_ids = []
            for card in cards:
                user_card = {"user_id": user_id, "card_id": card.id}
                await UserCardService.add_user_card(
                    uow, UserCardAddDTO.model_validate(user_card)
                )
                card_ids.append(card.id)
            return card_ids
