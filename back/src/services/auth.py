from fastapi import Request, Response
from src.infrastructure.jwt import JWT


AUTH_HEADER_KEY = "Authorization"

class Auth:
    def __init__(self, request: Request):
        self.web_token = JWT
        self._is_authorized = False
        if request.headers.get(AUTH_HEADER_KEY):
            self._is_authorized = True

    def is_authorized(self) -> bool:
        return self._is_authorized

