from random import randint

from fastapi import Request, Response

from src.config import config
from src.infrastructure.jwt import JWT
from src.infrastructure.redis import Redis, redis_helper
import json

AUTH_HEADER_KEY = "Authorization"


def get_email_otp_key(email):
    return f"otp:{email}"


def get_email_ghost_user_key(email: str):
    return f"ghost_user:{email}"


class Auth:
    def __init__(self, request: Request):
        self.web_token = JWT
        self._is_authorized = False
        if request.headers.get(AUTH_HEADER_KEY):
            self._is_authorized = True

    def is_authorized(self) -> bool:
        return self._is_authorized


def generate_otp_code() -> str:
    return str(randint(100000, 999999))


class OtpStorage:
    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    async def save_otp(email: str):
        redis = await redis_helper.get_redis()
        await redis.set(
            get_email_otp_key(email),
            generate_otp_code(),
            ex=config.otp.expire_minutes * 60,
        )

    @staticmethod
    async def verify_otp(email: str, otp: str) -> bool:
        redis = await redis_helper.get_redis()
        storage_otp = redis.get(get_email_otp_key(email))
        if storage_otp and storage_otp == otp:
            return True
        return False
