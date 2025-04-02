from dto import RoadmapAddDTO, RoadmapEditDTO
from utils.unitofwork import IUnitOfWork


class RoadmapsService:
    async def add_roadmap(self, uow: IUnitOfWork, roadmap: RoadmapAddDTO):
        roadmap_dict = roadmap.model_dump()
        async with uow:
            roadmap_id = await uow.roadmaps.add_one(roadmap_dict)
            await uow.commit()
            return roadmap_id

    async def edit_roadmap(self, uow: IUnitOfWork, roadmap_id: int , roadmap: RoadmapEditDTO):
        roadmap_dict = roadmap.model_dump()
        async with uow:
            await uow.roadmaps.edit_one(roadmap_id)

            await uow.roadmaps.edit_one(roadmap_id, roadmap_dict)
            await uow.commit()

    async def get_roadmaps(self, uow: IUnitOfWork):
        async with uow:
            roadmaps = await uow.roadmaps.find_all()
            return roadmaps

