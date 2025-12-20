from typing import Annotated

from fastapi import Depends, Request, Response

from src.models.db import AsyncSession, db_helper
from src.services.auth import Auth
from src.services.redis.redis import Redis, redis_helper
from src.services.user import UserRepo

RedisDep = Annotated[Redis, Depends(redis_helper.get_redis)]
SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]


async def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(session)


UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]


async def get_auth(request: Request, response: Response):
    return Auth(request, response)


AuthDep = Annotated[Auth, Depends(get_auth)]
