from typing import Annotated

from fastapi import Depends

from src.models.db import AsyncSession, db_helper
from src.services.user import UserRepo
from src.infrastructure.redis import Redis, redis_helper
from src.services.auth import OtpStorage


SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]


async def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(session)


UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]


RedisDep = Annotated[Redis, redis_helper.get_redis]


async def get_otp_storage(redis: RedisDep):
    return OtpStorage(redis)


OtpStorageDep = Annotated[OtpStorage, Depends(get_otp_storage)]
