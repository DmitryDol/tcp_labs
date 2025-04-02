from datetime import datetime
from pydantic import BaseModel

class UserAddDTO(BaseModel):
    name: str
    login: str
    password_hash: str
    avatar: str

class UserDTO(UserAddDTO):
    id: int
    created_at: datetime

class UserEditDTO(BaseModel):
    id: int
    password_hash: str
    avatar: str

class RoadmapAddDTO(BaseModel):
    owner_id: int
    title: str
    description: str
    difficulty: str
    edit_permission: str
    visibility: str

class RoadmapDTO(RoadmapAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

class RoadmapEditDTO(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    edit_permission: str
    visibility: str
   
class CardAddDTO(BaseModel):
    roadmap_id: int
    title: str
    description: str
    order_position: int

class CardDTO(CardAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

class CardEditDTO(BaseModel):
    id: int
    title: str
    description: str
    order_position: int    

class UserRoadmapAddDTO(BaseModel):
    user_id: int
    roadmap_id: int

class UserRoadmapDTO(UserRoadmapAddDTO):
    background: str

class UserRoadmapEditDTO(BaseModel):
    user_id: int
    roadmap_id: int
    background: str

class UserCardAddDTO(BaseModel):
    user_id: int
    card_id: int

class UserCardDTO(UserCardAddDTO):
    status: str

class UserCardEditDTO(BaseModel):
    user_id: int
    card_id: int
    status: str

class CardLinkAddDTO(BaseModel):
    card_id: int
    link_title: str
    link_content: str

class CardLinkDTO(CardLinkAddDTO):
    id: int

class CardLinkEditDTO(BaseModel):
    id: int
    link_title: str
    link_content: str

class CardExtendedDTO(CardDTO):
    links: list[CardLinkDTO]

class RoadmapExtendedDTO(RoadmapDTO):
    cards: list[CardExtendedDTO]