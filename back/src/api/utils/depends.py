from typing import Annotated

from fastapi import Depends, Request, Response

from src.models.db import AsyncSession, db_helper
from src.models.models import User as UserModel, Deck as DeckModel, Card as CardModel
from src.services.auth import Auth
from src.services.redis.redis import Redis, redis_helper
from src.services.crud import UserRepo
from src.services.crud import DeckRepo
from src.schemas.user import UserCreate, GhostUser, User
from src.schemas.deck import GhostDeck, DeckCreate, Deck
from src.services.schedule import Schedule


SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]


async def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(
        session,
        model=UserModel,
        schema=User,
        ghost_schema=GhostUser,
        schema_create=UserCreate,
    )


async def get_auth(request: Request, response: Response):
    return Auth(request, response)


async def get_deck_repo(session: SessionDep) -> DeckRepo:
    return DeckRepo(
        session,
        model=DeckModel,
        schema=Deck,
        ghost_schema=GhostDeck,
        schema_create=DeckCreate,
    )

async def get_schedule(session: SessionDep) -> Schedule:
    return Schedule(session)


AuthDep = Annotated[Auth, Depends(get_auth)]
UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]
DeckRepoDep = Annotated[DeckRepo, Depends(get_deck_repo)]
RedisDep = Annotated[Redis, Depends(redis_helper.get_redis)]
ScheduleDep = Annotated[Schedule, Depends(get_schedule)]
