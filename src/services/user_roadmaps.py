from typing import Dict
from dto import UserRoadmapAddDTO, UserRoadmapEditDTO
from utils.unitofwork import IUnitOfWork


class UserRoadmapsService:
    @staticmethod
    async def add_user_roadmap(uow: IUnitOfWork, user_roadmap: UserRoadmapAddDTO):
        user_roadmap_dict = user_roadmap.model_dump()
        async with uow:
            user_roadmap_id = await uow.user_roadmaps.add_one(user_roadmap_dict)
            await uow.commit()
            return user_roadmap_id

    @staticmethod
    async def edit_user_roadmap(uow: IUnitOfWork, user_roadmap_id: int , user_roadmap: UserRoadmapEditDTO):
        user_roadmap_dict = user_roadmap.model_dump(exclude_unset=True)
        async with uow:
            await uow.user_roadmaps.edit_one(user_roadmap_id, user_roadmap_dict)
            await uow.commit()

    @staticmethod
    async def get_user_roadmaps(uow: IUnitOfWork):
        async with uow:
            user_roadmaps = await uow.user_roadmaps.find_all()
            return user_roadmaps
        
    @staticmethod
    async def delete_user_roadmap(uow: IUnitOfWork, user_roadmap_id: Dict[str, int]):
        async with uow:
            user_roadmap = await uow.user_roadmaps.delete_one(user_roadmap_id)
            await uow.commit()
            return user_roadmap
