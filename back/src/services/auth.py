from fastapi import Request, Response
from src.utils.jwt import JWT

AUTH_HEADER_KEY = "Authorization"


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
