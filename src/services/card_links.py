from dto import CardLinkAddDTO, CardLinkDTO, CardLinkEditDTO
from utils.unitofwork import IUnitOfWork

class CardLinksService:
    @staticmethod
    async def add_card_link(uow: IUnitOfWork, card_link: CardLinkAddDTO):
        card_link_dict = card_link.model_dump()
        async with uow:
            card_link_id = await uow.card_links.add_one(card_link_dict)
            await uow.commit()
            return card_link_id

    @staticmethod
    async def edit_card_link(uow: IUnitOfWork, card_link_id: int , card_link: CardLinkEditDTO):
        card_link_dict = card_link.model_dump(exclude_unset=True)
        async with uow:
            card_link_id = await uow.card_links.edit_one(card_link_id, card_link_dict)
            await uow.commit()
            return card_link_id

    @staticmethod
    async def get_card_links(uow: IUnitOfWork) -> CardLinkDTO:
        async with uow:
            card_links = await uow.card_links.find_all()
            return card_links
        
    @staticmethod
    async def get_card_link(uow: IUnitOfWork, card_link_id: int) -> CardLinkDTO:
        async with uow:
            card_links = await uow.card_links.find_one(card_link_id)
            return card_links
        
    @staticmethod
    async def delete_card_link(uow: IUnitOfWork, card_link_id: int):
        async with uow:
            card_link = await uow.card_links.delete_one(card_link_id)
            await uow.commit()
            return card_link
