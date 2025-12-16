from typing import Annotated

from fastapi import Depends, Request, Response

from src.models.db import AsyncSession, db_helper
from src.services.user import UserRepo
from src.services.redis import Redis, redis_helper
from src.services.auth import Auth, LoginOtpStorage, RegisterOtpStrogare


SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]


async def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(session)


UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]


RedisDep = Annotated[Redis, Depends(redis_helper.get_redis)]


async def get_login_otp_storage(redis: RedisDep):
    return LoginOtpStorage(redis)

async def get_register_otp_storage(redis: RedisDep):
    return RegisterOtpStrogare(redis)


LoginOtpStorageDep = Annotated[LoginOtpStorage, Depends(get_login_otp_storage)]
RegisterOtpStorageDep = Annotated[RegisterOtpStrogare, Depends(get_register_otp_storage)]


async def get_auth(request: Request, response: Response):
    return Auth(request, response)


AuthDep = Annotated[Auth, Depends(get_auth)]
