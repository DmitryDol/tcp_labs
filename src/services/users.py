from typing import Any, Dict, Optional
from dto import UserAddDTO, UserEditDTO
from utils.unitofwork import IUnitOfWork


class UsersService:
    @staticmethod
    async def add_user(uow: IUnitOfWork, user: UserAddDTO):
        user_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    @staticmethod
    async def edit_user(uow: IUnitOfWork, user_id: int , user: UserEditDTO):
        user_dict = user.model_dump(exclude_unset=True)
        async with uow:
            await uow.users.edit_one(user_id, user_dict)
            await uow.commit()

    @staticmethod
    async def get_user(uow: IUnitOfWork, filter_by: Optional[Dict[str, Any]] = None):
        async with uow:
            users = await uow.users.find_one({"id": filter_by})
            return users

    @staticmethod
    async def get_users(uow: IUnitOfWork, filter_by: Optional[Dict[str, Any]] = None):
        async with uow:
            users = await uow.users.find_all({"id": filter_by})
            return users
        
    @staticmethod
    async def delete_user(uow: IUnitOfWork, user_id: int):
        async with uow:
            user = await uow.users.delete_one(user_id)
            await uow.commit()
            return user
