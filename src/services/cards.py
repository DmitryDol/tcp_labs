from dto import CardAddDTO, CardEditDTO, CardExtendedDTO
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
    async def edit_card(uow: IUnitOfWork, card_id: int , card: CardEditDTO):
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
    async def delete_card(uow: IUnitOfWork, card_id: int):
        async with uow:
            card = await uow.cards.delete_one(card_id)
            await uow.commit()
            return card
        
    @staticmethod
    async def get_card_extended(uow: IUnitOfWork, card_id: int):
        async with uow:
            card = await uow.cards.find_one(id = card_id)
            card_dict = card.model_dump()
            card_links = await uow.card_links.find_all({"card_id": card.id})
            card_dict["links"] = [None]
            for i, card_link in enumerate(card_links, start=0):
                card_dict["links"][i] = card_link.model_dump()
            extended_card = CardExtendedDTO.model_validate(card_dict, from_attributes=True)
            return extended_card
