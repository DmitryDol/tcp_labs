from dto import CardsAddDTO, CardsEditDTO
from utils.unitofwork import IUnitOfWork


class cardsService:
    async def add_card(self, uow: IUnitOfWork, card: CardsAddDTO):
        card_dict = card.model_dump()
        async with uow:
            card_id = await uow.cards.add_one(card_dict)
            await uow.commit()
            return card_id

    async def edit_card(self, uow: IUnitOfWork, card_id: int , card: CardsEditDTO):
        card_dict = card.model_dump()
        async with uow:
            await uow.cards.edit_one(card_id)

            await uow.cards.edit_one(card_id, card_dict)
            await uow.commit()

    async def get_cards(self, uow: IUnitOfWork):
        async with uow:
            cards = await uow.cards.find_all()
            return cards
        
    async def delete_card(self, uow: IUnitOfWork, card_id: int):
        async with uow:
            card = await uow.cards.delete_one(card_id)
            return card
