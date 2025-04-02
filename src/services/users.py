from dto import UsersAddDTO, UsersEditDTO
from utils.unitofwork import IUnitOfWork


class UsersService:
    async def add_user(self, uow: IUnitOfWork, user: UsersAddDTO):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    async def edit_user(self, uow: IUnitOfWork, user_id: int , user: UsersEditDTO):
        user_dict = user.model_dump()
        async with uow:
            await uow.users.edit_one(user_id)

            await uow.users.edit_one(user_id, user_dict)
            await uow.commit()

    async def get_users(self, uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users
        
    async def delete_user(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            user = await uow.users.delete_one(user_id)
            return user
