from random import randint

from fastapi import Request, Response

from src.config import config
from src.infrastructure.jwt import JWT
from src.infrastructure.redis import Redis, redis_helper
from src.infrastructure.password import PasswordHelper as ph

AUTH_HEADER_KEY = "Authorization"



def get_email_ghost_user_key(email: str):
    return f"ghost_user:{email}"


class Auth:
    def __init__(self, request: Request, response: Response):
        self.web_token = JWT
        self.request = request
        self.response = response
        
    def is_authorized(self) -> bool:
        if auth_token := self.request.headers.get(AUTH_HEADER_KEY):
            if auth_token:
                return True
        return False

        return self._is_authorized

    def login(self, user):
        # self.response.headers[AUTH_HEADER_KEY]
        ...

    def get_refresh(self):
        ...

    def get_token_user_id(self, token: str) -> int:
        ...

    def verify_refresh(self, refresh: str) -> bool:
        ...
    
    def refresh(self):
        ...


def generate_otp_code() -> str:
    return str(randint(100000, 999999))


class OtpStorage:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_email_otp_key(self, email):
        return f"otp:{email}"

    async def save_otp(self, email: str, otp: str):
        await self.redis.set(
            self.get_email_otp_key(email),
            ph.hash_password(otp),
            ex=config.otp.expire_minutes * 60,
        )

    async def verify_otp(self, email: str, otp: str) -> bool:
        storage_otp = await self.redis.get(self.get_email_otp_key(email))
        if storage_otp and ph.verify_password(storage_otp, otp):
            return True
        return False


async def send_otp(email: str):
    ...
