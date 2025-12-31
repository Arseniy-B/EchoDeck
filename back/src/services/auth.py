from fastapi import Request, Response, Cookie
from src.utils.jwt import JWT
from src.config import config


AUTH_HEADER_KEY = "authorization"
REFRESH_COOKIE_KEY = "refresh_token"


class Auth:
    def __init__(self, request: Request, response: Response):
        self.web_token = JWT
        self.request = request
        self.response = response

    def get_refresh(self) -> str | None: 
        if REFRESH_COOKIE_KEY in self.request.cookies:
            return self.request.cookies[REFRESH_COOKIE_KEY]

    def get_access(self) -> str | None:
        return self.request.headers[AUTH_HEADER_KEY]

    def is_refresh(self) -> int | None:
        if auth_token := self.get_refresh():
            if user_id := JWT.decode(auth_token):
                return user_id

    def is_authorized(self) -> int | None:
        if auth_token := self.get_access():
            if user_id := JWT.decode(auth_token):
                return user_id

    def login(self, user_id: int):
        access = JWT.encode(user_id)
        self.response.headers[AUTH_HEADER_KEY] = access

        refresh = JWT.encode(
            user_id, expire_minutes=config.jwt.refresh_token_expire_minutes
        )
        self.response.set_cookie(
            key=REFRESH_COOKIE_KEY,
            value=refresh,
            httponly=True,
            max_age=config.jwt.refresh_token_expire_minutes * 60,
        )

    def refresh(self, user_id): 
        new_access = JWT.encode(user_id)
        self.response.headers[AUTH_HEADER_KEY] = new_access

