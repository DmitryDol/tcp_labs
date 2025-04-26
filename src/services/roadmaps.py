import logging

from fastapi import HTTPException
from dto import RoadmapAddDTO, RoadmapDTO, RoadmapEditDTO, RoadmapExtendedDTO, UserRoadmapEditDTO
from services.cards import CardsService
from utils.unitofwork import IUnitOfWork
from typing import List, Optional


logger = logging.getLogger(__name__)

class RoadmapsService:
    @staticmethod
    async def add_roadmap(uow: IUnitOfWork, roadmap: RoadmapAddDTO):
        roadmap_dict = roadmap.model_dump()
        async with uow:
            roadmap_id = await uow.roadmaps.add_one(roadmap_dict)
            await uow.commit()
            owner_id = (await RoadmapsService.get_roadmap(uow, roadmap_id)).owner_id
            return roadmap_id, owner_id

    @staticmethod
    async def edit_roadmap(uow: IUnitOfWork, roadmap_id: int , roadmap: RoadmapEditDTO):
        roadmap_dict = roadmap.model_dump(exclude_unset=True)
        async with uow:
            await uow.roadmaps.edit_one(roadmap_id, roadmap_dict)
            await uow.commit()

    @staticmethod
    async def get_roadmap(uow: IUnitOfWork, filter_by: int) -> RoadmapDTO:
        async with uow:
            roadmaps = await uow.roadmaps.find_one(id=filter_by)
            return roadmaps
        
    @staticmethod
    async def get_roadmap_extended(uow: IUnitOfWork, roadmap_id: int):
        async with uow:
            roadmap = await uow.roadmaps.find_one(id=roadmap_id)
            
            if not roadmap:
                raise HTTPException(status_code=404, detail="Roadmap not found")
            
            roadmap_dict = roadmap.model_dump()
            cards = await uow.cards.find_all({"roadmap_id": roadmap_id})
            roadmap_dict["cards"] = []
            for card in cards:
                roadmap_dict["cards"].append(await CardsService.get_card_extended(uow, card.id))
            logger.debug('\n\n\n', roadmap_dict, '\n\n\n')
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
        
    @staticmethod
    async def delete_roadmap(uow: IUnitOfWork, roadmap_id: int):
        async with uow:
            roadmap = await uow.roadmaps.delete_one(roadmap_id)
            await uow.commit()
            return roadmap
        
    @staticmethod
    async def link_user_to_roadmap(uow: IUnitOfWork, roadmap_id: int, user_id: int):
        async with uow:
            await uow.user_roadmaps.add_one({"roadmap_id": roadmap_id, "user_id": user_id})
            await uow.commit()

    @staticmethod
    async def change_background(uow: IUnitOfWork, roadmap_id: int, user_id: int, background: UserRoadmapEditDTO):
        async with uow:
            await uow.user_roadmaps.edit_one(
                id_or_filter={"roadmap_id": roadmap_id, "user_id": user_id},
                data=background
            )