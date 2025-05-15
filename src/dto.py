from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TokenDTO(BaseModel):
    access_token: str
    token_type: str

class LoginDTO(TokenDTO):
    login: str
    username: str

class UserAuthDTO(BaseModel):
    id: int
    name: str
    login: str
    password_hash: str

class UserAddDTO(BaseModel):
    name: str
    login: str
    password_hash: str

class UserDTO(BaseModel):
    id: int
    name: str
    login: str
    created_at: datetime
    avatar: str

class UserEditDTO(BaseModel):
    name: Optional[str] = None
    password_hash: Optional[str] = None
    avatar: Optional[str] = None

class SimplifiedRoadmapDTO(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str

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
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    edit_permission: Optional[str] = None
    visibility: Optional[str] = None
   
class CardAddDTO(BaseModel):
    roadmap_id: int
    title: str
    description: Optional[str]
    order_position: int

class CardDTO(CardAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

class CardEditDTO(BaseModel):
    title: Optional[str]
    description: Optional[str]
    order_position: Optional[int]

class UserRoadmapAddDTO(BaseModel):
    user_id: int
    roadmap_id: int

class UserRoadmapDTO(UserRoadmapAddDTO):
    background: str

class UserRoadmapEditDTO(BaseModel):
    background: str

class UserCardAddDTO(BaseModel):
    user_id: int
    card_id: int

class UserCardDTO(UserCardAddDTO):
    status: str

class UserCardEditDTO(BaseModel):
    status: str

class CardLinkAddDTO(BaseModel):
    card_id: int
    link_title: str
    link_content: str

class CardLinkDTO(CardLinkAddDTO):
    id: int

class CardLinkEditDTO(BaseModel):
    link_title: Optional[str]
    link_content: Optional[str]

class CardExtendedDTO(CardDTO):
    links: list[Optional[CardLinkDTO]]

class RoadmapExtendedDTO(RoadmapDTO):
    cards: list[Optional[CardExtendedDTO]]