from dto import cardsAddDTO, cardsEditDTO
from utils.unitofwork import IUnitOfWork


class cardsService:
    async def add_card(self, uow: IUnitOfWork, card: cardsAddDTO):
        card_dict = card.model_dump()
        async with uow:
            card_id = await uow.cards.add_one(card_dict)
            await uow.commit()
            return card_id

    async def edit_card(self, uow: IUnitOfWork, card_id: int , card: cardsEditDTO):
        card_dict = card.model_dump()
        async with uow:
            await uow.cards.edit_one(card_id)

            await uow.cards.edit_one(card_id, card_dict)
            await uow.commit()

    async def get_cards(self, uow: IUnitOfWork):
        async with uow:
            cards = await uow.cards.find_all()
            return cards
