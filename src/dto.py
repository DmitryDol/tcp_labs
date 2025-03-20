from datetime import datetime
from sqlalchemy import DateTime
from pydantic import BaseModel, ConfigDict

class UsersAddDTO(BaseModel):
    name: str
    login: str
    password_hash: str
    avatar: str

class UsersDTO(UsersAddDTO):
    user_id: int

class RoadmapAddDTO(BaseModel):
    owner_id: int
    title: str
    description: str
    difficulty: str
    edit_permission: str
    visibility: str

class RoadmapDTO(RoadmapAddDTO):
    roadmap_id: int
   
class CardAddDTO(BaseModel):
    roadmap_id: int
    title: str
    description: str
    order_position: int

class CardDTO(CardAddDTO):
    card_id: int

class UserRoadmapAddDTO(BaseModel):
    user_id: int
    roadmap_id: int

class UserRoadmapDTO(UserRoadmapAddDTO):
    background: str

class UserCardAddDTO(BaseModel):
    user_id: int
    card_id: int

class UserCardDTO(UserCardAddDTO):
    status: str

class CardLinkAddDTO(BaseModel):
    card_id: int
    link_title: str
    link_content: str

class CardLinkDTO(CardLinkAddDTO):
    id: int