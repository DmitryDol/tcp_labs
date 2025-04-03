from typing import Annotated, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path
from dto import CardAddDTO, CardEditDTO
from api.dependencies import UOWDep
#from queries.orm import User
from services.cards import CardsService
#from src import crud
from database import async_session_factory

router = APIRouter(
    prefix="/cards", 
    tags=["cards"]
)


@router.post("")
async def add_card(
    card: CardAddDTO,
    uow: UOWDep,
):
    card_id = await CardsService.add_user(uow, card)
    return {"card_id": card_id}

@router.get("/{card_id}")
async def get_user_info(
    card_id: Annotated[int, Path(title="Card id")],
    uow: UOWDep
):
    card = await CardsService.get_cards(uow=uow, filter_by=card_id)
    return card

@router.delete(
        "",
        status_code=204
)
async def delete_card(
    card_id: int,
    uow: UOWDep
):
    await CardsService.delete_card(uow, card_id)

@router.patch("/{user_id}")
async def edit_card(
    card_id: int,
    card: CardEditDTO,
    uow: UOWDep
):
    await CardsService.edit_card(uow, card_id, card)
    return {"card_id": card_id}