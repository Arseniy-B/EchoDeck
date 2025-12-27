from fastapi import APIRouter, HTTPException, status
from src.api.utils.depends import AuthDep, CardRepoDep
from src.schemas.card import CardCreate, CardCreateData, Card, GhostCard
from datetime import datetime


router = APIRouter(prefix="/card")


@router.post("/create")
async def add_card(
    card_create_data: CardCreateData, auth: AuthDep, card_repo: CardRepoDep
):
    user_id = auth.is_authorized()
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    card_create = CardCreate.model_validate(
        {
            **card_create_data.model_dump(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    )
    await card_repo.create(card_create)
