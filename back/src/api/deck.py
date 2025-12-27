from fastapi import APIRouter, HTTPException, status
from src.schemas.deck import DeckCreate, DeckCreateData
from src.api.utils.depends import AuthDep, DeckRepoDep


router = APIRouter(prefix="/deck")


@router.post("/create")
async def add_deck(deck_create_data: DeckCreateData, auth: AuthDep, Deck: DeckRepoDep):
    user_id = auth.is_authorized()
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    deck_create = DeckCreate.model_validate({**deck_create_data.model_dump(), "user_id": user_id})

    await Deck.create(deck_create)


@router.get("/")
async def get_decks(auth: AuthDep, Deck: DeckRepoDep):
    user_id = auth.is_authorized()
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return Deck.get_all(user_id)


@router.post("/delete")
async def delete(auth: AuthDep, Deck: DeckRepoDep, obj_id: int):
    user_id = auth.is_authorized()
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    obj = await Deck.get_by_id(obj_id)
    if obj.user_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    await Deck.delete(obj_id)

