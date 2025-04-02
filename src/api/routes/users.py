from typing import Any
from fastapi import APIRouter, Depends, HTTPException

from src import crud
from src.database import async_session_factory

router = APIRouter(
    prefix="/users", 
    tags=["users"]
)


@router.post("/")
async def add_user(
    user: User
)