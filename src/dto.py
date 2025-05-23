from datetime import datetime

from pydantic import BaseModel


class TokenDTO(BaseModel):
    access_token: str
    token_type: str


class LoginDTO(TokenDTO):
    id: int
    login: str
    username: str
    avatar: str


class UserAuthDTO(BaseModel):
    id: int
    name: str
    login: str
    password_hash: str
    avatar: str


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
    name: str | None = None
    password_hash: str | None = None
    avatar: str | None = None


class SimplifiedRoadmapDTO(BaseModel):
    owner_id: int
    id: int
    title: str
    description: str
    difficulty: str
    # current_page: int
    # last_page: int


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
    title: str | None = None
    description: str | None = None
    difficulty: str | None = None
    edit_permission: str | None = None
    visibility: str | None = None


class CardAddDTO(BaseModel):
    roadmap_id: int
    title: str
    description: str | None = None
    order_position: int


class CardDTO(CardAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime


class CardEditDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    order_position: int | None = None


class UserRoadmapAddDTO(BaseModel):
    user_id: int
    roadmap_id: int


class UserRoadmapAddExtendedDTO(UserRoadmapAddDTO):
    card_ids: list[int] | None = None


class UserRoadmapDTO(UserRoadmapAddDTO):
    background: str


class BackgroundDTO(BaseModel):
    background: str | None = None


class AvatarDTO(BaseModel):
    avatar: str


class UserRoadmapEditDTO(BaseModel):
    background: str


class UserCardAddDTO(BaseModel):
    user_id: int
    card_id: int


class UserCardDTO(UserCardAddDTO):
    status: str


class UserCardEditDTO(BaseModel):
    status: str


class UserCardEditWithUserIdDTO(UserCardEditDTO):
    card_id: int


class CardLinkAddDTO(BaseModel):
    card_id: int
    link_title: str
    link_content: str


class CardLinkDTO(CardLinkAddDTO):
    id: int


class CardLinkEditDTO(BaseModel):
    link_title: str | None = None
    link_content: str | None = None


class CardExtendedDTO(CardDTO):
    links: list[CardLinkDTO | None] = []
    status: str | None = None


class RoadmapExtendedDTO(RoadmapDTO):
    cards: list[CardExtendedDTO | None] = []


class PaginatedRoadmapsDTO(BaseModel):
    roadmaps: list[SimplifiedRoadmapDTO | None] = []
    total_pages: int
