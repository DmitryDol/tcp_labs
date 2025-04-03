import enum
from api.routes import roadmaps
from dto import RoadmapAddDTO, RoadmapDTO, RoadmapEditDTO, RoadmapExtendedDTO
from utils.unitofwork import IUnitOfWork
from typing import List, Optional, Dict, Any


class RoadmapsService:
    @staticmethod
    async def add_roadmap(uow: IUnitOfWork, roadmap: RoadmapAddDTO):
        roadmap_dict = roadmap.model_dump()
        async with uow:
            roadmap_id = await uow.roadmaps.add_one(roadmap_dict)
            await uow.commit()
            owner_id = RoadmapsService.get_roadmap(roadmap_id).owner_id
            return roadmap_id, owner_id

    @staticmethod
    async def edit_roadmap(uow: IUnitOfWork, roadmap_id: int , roadmap: RoadmapEditDTO):
        roadmap_dict = roadmap.model_dump(exclude_unset=True)
        async with uow:
            await uow.roadmaps.edit_one(roadmap_id, roadmap_dict)
            await uow.commit()

    @staticmethod
    async def get_roadmap(uow: IUnitOfWork, filter_by: Optional[Dict[str, Any]] = None) -> RoadmapDTO:
        async with uow:
            roadmaps = await uow.roadmaps.find_one({"id": filter_by})
            return roadmaps
        
    @staticmethod
    async def get_roadmap_extended(uow: IUnitOfWork, roadmap_id: int):
        async with uow:
            roadmap = await uow.roadmaps.find_one({"id": roadmap_id})
            cards = await uow.cards.find_all({"roadmap_id": roadmap_id})
            roadmap_dict = roadmap.model_dump()
            roadmap_dict["cards"] = cards.model_dump()
            for i, card in enumerate(cards, start=0):
                card_links = await uow.card_links.find_all({"card_id": card.id})
                roadmap_dict["cards"][i]["links"] = card_links
            extended_roadmap = RoadmapExtendedDTO.model_validate(roadmap_dict, from_attributes=True)
            return extended_roadmap


    @staticmethod
    async def get_public_roadmaps(
        uow: IUnitOfWork, 
        search: Optional[str] = None, 
        difficulty: Optional[str] = None, 
        limit: Optional[int] = None
    ) -> List[RoadmapDTO]:
        """
        Gets public roadmaps with search and filtering capabilities 
        
        Args:
            uow: Unit of Work instance
            search: Optional str for searching by title
            difficulty: Optional filter by roadmap difficulty can be 'easy', 'medium' or 'hard'
            limit: Optional limit on the number of roadmaps returned
        
        Returns:
            List of the RoadmapDTO objects
        """
        async with uow:
            roadmaps = await uow.roadmaps.find_public_roadmaps(
                search=search, 
                difficulty=difficulty, 
                limit=limit
            )
            return roadmaps
        
    @staticmethod
    async def delete_roadmap(uow: IUnitOfWork, roadmap_id: int):
        async with uow:
            roadmap = await uow.roadmaps.delete_one(roadmap_id)
            await uow.commit()
            return roadmap
