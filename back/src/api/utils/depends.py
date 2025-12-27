from typing import Annotated

from fastapi import Depends, Request, Response

from src.models.db import AsyncSession, db_helper
from src.models.models import User as UserModel, Deck as DeckModel, Card as CardModel
from src.services.auth import Auth
from src.services.redis.redis import Redis, redis_helper
from src.services.user import UserRepo
from src.services.deck import DeckRepo
from src.schemas.user import UserCreate, GhostUser, User
from src.schemas.deck import GhostDeck, DeckCreate, Deck
from src.schemas.card import Card, GhostCard, CardCreate
from src.services.card import CardRepo


RedisDep = Annotated[Redis, Depends(redis_helper.get_redis)]
SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]


async def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(
        session,
        model=UserModel,
        schema=User,
        ghost_schema=GhostUser,
        schema_create=UserCreate,
    )


UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]


async def get_auth(request: Request, response: Response):
    return Auth(request, response)


AuthDep = Annotated[Auth, Depends(get_auth)]


async def get_deck_repo(session: SessionDep) -> DeckRepo:
    return DeckRepo(
        session,
        model=DeckModel,
        schema=Deck,
        ghost_schema=GhostDeck,
        schema_create=DeckCreate,
    )


DeckRepoDep = Annotated[DeckRepo, Depends(get_deck_repo)]


async def get_card_repo(session: SessionDep) -> CardRepo:
    return CardRepo(
        session=session,
        model=CardModel,
        schema=Card,
        ghost_schema=GhostCard,
        schema_create=CardCreate,
    )


CardRepoDep = Annotated[CardRepo, Depends(get_card_repo)]
