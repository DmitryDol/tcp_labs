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
            users = await uow.users.find_one(id=filter_by)
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

    @staticmethod
    async def get_linked_roadmaps(
        uow: IUnitOfWork,
        user_id: int, 
        search: Optional[str] = None, 
        difficulty: Optional[str] = None, 
        limit: Optional[int] = None
    ):
        """
        Gets roadmaps linked to user_id with search and filtering capabilities 
        
        Args:
            uow: Unit of Work instance
            user_id: id of the user
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty can be 'easy', 'medium' or 'hard'
            limit: Optional limit on the number of roadmaps returned
        
        Returns:
            List of the simplified roadmap dictionaries
        """
        async with uow:
            user_roadmaps_list = await uow.user_roadmaps.find_all({"user_id": user_id})

            roadmaps = await uow.roadmaps.find_user_roadmaps(
                user_roadmaps_list=user_roadmaps_list,
                search=search, 
                difficulty=difficulty, 
                limit=limit
            )
            
            simplified_roadmaps = [
                {
                    "roadmap_id": roadmap.id,
                    "title": roadmap.title,
                    "description": roadmap.description,
                    "difficulty": roadmap.difficulty.value if hasattr(roadmap.difficulty, 'value') else roadmap.difficulty
                }
                for roadmap in roadmaps
            ]
            
            return simplified_roadmaps
