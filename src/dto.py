from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class UsersAddDTO(BaseModel):
    name: str
    login: str
    password_hash: str
    avatar: str


class UsersDTO(UsersAddDTO):
    user_id: int