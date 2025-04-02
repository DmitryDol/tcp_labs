from dto import UserRoadmapAddDTO, UserRoadmapEditDTO
from utils.unitofwork import IUnitOfWork


class user_roadmapsService:
    async def add_user_roadmap(self, uow: IUnitOfWork, user_roadmap: UserRoadmapAddDTO):
        user_roadmap_dict = user_roadmap.model_dump()
        async with uow:
            user_roadmap_id = await uow.user_roadmaps.add_one(user_roadmap_dict)
            await uow.commit()
            return user_roadmap_id

    async def edit_user_roadmap(self, uow: IUnitOfWork, user_roadmap_id: int , user_roadmap: UserRoadmapEditDTO):
        user_roadmap_dict = user_roadmap.model_dump()
        async with uow:
            await uow.user_roadmaps.edit_one(user_roadmap_id)

            await uow.user_roadmaps.edit_one(user_roadmap_id, user_roadmap_dict)
            await uow.commit()

    async def get_user_roadmaps(self, uow: IUnitOfWork):
        async with uow:
            user_roadmaps = await uow.user_roadmaps.find_all()
            return user_roadmaps
        
    async def delete_user_roadmap(self, uow: IUnitOfWork, user_roadmap_id: int):
        async with uow:
            user_roadmap = await uow.user_roadmaps.delete_one(user_roadmap_id)
            return user_roadmap
