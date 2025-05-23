from dto import CardAddDTO, CardDTO, CardEditDTO, CardExtendedDTO, UserCardDTO
from utils.unitofwork import IUnitOfWork


class CardsService:
    @staticmethod
    async def add_card(uow: IUnitOfWork, card: CardAddDTO):
        card_dict = card.model_dump()
        async with uow:
            card_id = await uow.cards.add_one(card_dict)
            await uow.commit()
            return card_id

    @staticmethod
    async def edit_card(uow: IUnitOfWork, card_id: int, card: CardEditDTO):
        card_dict = card.model_dump(exclude_unset=True)
        async with uow:
            await uow.cards.edit_one(card_id, card_dict)
            await uow.commit()

    @staticmethod
    async def get_cards(uow: IUnitOfWork):
        async with uow:
            cards = await uow.cards.find_all()
            return cards

    @staticmethod
    async def get_card(uow: IUnitOfWork, card_id) -> CardDTO | None:
        async with uow:
            card = await uow.cards.find_one(id=card_id)
            return card

    @staticmethod
    async def delete_card(uow: IUnitOfWork, card_id: int):
        async with uow:
            card = await uow.cards.delete_one(card_id)
            await uow.commit()
            return card

    @staticmethod
    async def get_card_extended(
        uow: IUnitOfWork, card_id: int, user_id: int
    ) -> CardExtendedDTO | None:
        async with uow:
            card = await uow.cards.find_one(id=card_id)

            if card is None:
                return None

            card_dict = card.model_dump()
            card_links = await uow.card_links.find_all({"card_id": card.id})

            card_dict["links"] = [
                card_link.model_dump() for card_link in (card_links or [])
            ]

            card_status: UserCardDTO = await uow.user_cards.find_one(
                user_id=user_id, card_id=card_id
            )
            card_dict["status"] = card_status and card_status.status

            extended_card = CardExtendedDTO.model_validate(
                card_dict, from_attributes=True
            )
            return extended_card
