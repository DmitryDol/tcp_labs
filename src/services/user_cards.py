from dto import UserCardAddDTO, UserCardEditDTO
from utils.unitofwork import IUnitOfWork


class user_cardsService:
    async def add_user_card(self, uow: IUnitOfWork, user_card: UserCardAddDTO):
        user_card_dict = user_card.model_dump()
        async with uow:
            user_card_id = await uow.user_cards.add_one(user_card_dict)
            await uow.commit()
            return user_card_id

    async def edit_user_card(self, uow: IUnitOfWork, user_card_id: int , user_card: UserCardEditDTO):
        user_card_dict = user_card.model_dump()
        async with uow:
            await uow.user_cards.edit_one(user_card_id)

            await uow.user_cards.edit_one(user_card_id, user_card_dict)
            await uow.commit()

    async def get_user_cards(self, uow: IUnitOfWork):
        async with uow:
            user_cards = await uow.user_cards.find_all()
            return user_cards
        
    async def delete_user_card(self, uow: IUnitOfWork, user_card_id: int):
        async with uow:
            user_card = await uow.user_cards.delete_one(user_card_id)
            return user_card
