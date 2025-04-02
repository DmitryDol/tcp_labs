from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from queries.orm import User
from services import UserService
from src import crud
from src.database import async_session_factory

router = APIRouter(
    prefix="/users", 
    tags=["users"]
)


@router.post("/")
async def add_user(
    user: User,
    users_service: Annotated[UserService, Depends(users_service)],
)