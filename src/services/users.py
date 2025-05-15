from typing import Annotated, Any, Dict, List, Optional
from dto import UserAddDTO, UserAuthDTO, UserDTO, UserEditDTO
from utils.unitofwork import IUnitOfWork
from utils.utils import hash_password, verify_password


class UsersService:
    @staticmethod
    async def authenticate_user(uow: IUnitOfWork, login: str, password: str) -> UserAuthDTO:
        async with uow:
            user: UserAuthDTO = await uow.users.find_auth_info(login)
            if not user:
                return False
            if not verify_password(password, user.password_hash):
                return False
            return user

    @staticmethod
    async def add_user(uow: IUnitOfWork, user: UserAddDTO):
        user_dict = user.model_dump()
        user_dict["password_hash"] = hash_password(user_dict["password_hash"])
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
    async def get_user(uow: IUnitOfWork, filter_by: Optional[Dict[str, Any]] = None) -> UserDTO:
        async with uow:
            users = await uow.users.find_one(id=filter_by)
            return users

    @staticmethod
    async def get_users(uow: IUnitOfWork, filter_by: Optional[Dict[str, Any]] = None) -> List[UserDTO]:
        async with uow:
            users = await uow.users.find_all({"id": filter_by})
            return users
        
    @staticmethod
    async def delete_user(uow: IUnitOfWork, user_id: int):
        async with uow:
            user = await uow.users.delete_one(user_id)
            await uow.commit()
            return user

    
