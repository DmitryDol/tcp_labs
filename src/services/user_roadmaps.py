from typing import Dict, List, Optional
from dto import SimplifiedRoadmapDTO, UserRoadmapAddDTO, UserRoadmapDTO, UserRoadmapEditDTO
from utils.unitofwork import IUnitOfWork


class UserRoadmapsService:
    @staticmethod
    async def link_user_to_roadmap(uow: IUnitOfWork, roadmap_id: int, user_id: int) -> UserRoadmapAddDTO:
        async with uow:
            user_roadmap_id = await uow.user_roadmaps.add_one({"roadmap_id": roadmap_id, "user_id": user_id})
            await uow.commit()
            return UserRoadmapAddDTO.model_validate(user_roadmap_id, from_attributes=True)

    @staticmethod
    async def change_background(uow: IUnitOfWork, roadmap_id: int, user_id: int, background: UserRoadmapEditDTO):
        background_dict = background.model_dump(exclude_unset=True)
        async with uow:
            await uow.user_roadmaps.edit_one(
                id_or_filter={"roadmap_id": roadmap_id, "user_id": user_id},
                data=background_dict
            )
            await uow.commit()

    @staticmethod
    async def get_user_roadmaps(uow: IUnitOfWork, user_id: int):
        async with uow:
            user_roadmaps: List[UserRoadmapDTO] = await uow.user_roadmaps.find_all(user_id=user_id)
            roadmaps = [roadmap.roadmap_id for roadmap in user_roadmaps] 
            return roadmaps
        
    @staticmethod
    async def delete_user_roadmap(uow: IUnitOfWork, user_roadmap_id: Dict[str, int]):
        async with uow:
            user_roadmap = await uow.user_roadmaps.delete_one(user_roadmap_id)
            await uow.commit()
            return user_roadmap
        
    @staticmethod
    async def get_background(uow: IUnitOfWork, user_roadmap_id: Dict[str, int]) -> UserRoadmapDTO:
        async with uow:
            background = await uow.user_roadmaps.find_one(user_roadmap_id)
            return background

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
            roadmap_ids = [ur.roadmap_id for ur in user_roadmaps_list]

            roadmaps = await uow.roadmaps.find_user_roadmaps(
                roadmap_ids=roadmap_ids,
                search=search, 
                difficulty=difficulty, 
                limit=limit
            )
            
            simplified_roadmaps = [
                # {
                #     "roadmap_id": roadmap.id,
                #     "title": roadmap.title,
                #     "description": roadmap.description,
                #     "difficulty": roadmap.difficulty.value if hasattr(roadmap.difficulty, 'value') else roadmap.difficulty
                # },
                SimplifiedRoadmapDTO.model_validate(roadmap, from_attributes=True)
                for roadmap in roadmaps
            ]
            
            return simplified_roadmaps