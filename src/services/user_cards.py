from dto import UserCardAddDTO, UserCardEditDTO
from utils.unitofwork import IUnitOfWork


class user_cardsService:
    @staticmethod
    async def add_user_card(uow: IUnitOfWork, user_card: UserCardAddDTO):
        user_card_dict = user_card.model_dump()
        async with uow:
            user_card_id = await uow.user_cards.add_one(user_card_dict)
            await uow.commit()
            return user_card_id

    @staticmethod
    async def edit_user_card(uow: IUnitOfWork, user_card_id: int , user_card: UserCardEditDTO):
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
