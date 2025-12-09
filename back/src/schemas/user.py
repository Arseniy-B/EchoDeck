from pydantic import BaseModel


class EmailUserLogin(BaseModel):
    email: str
    otp: str

class PasswordUserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    password: str

class GhostUser(BaseModel):
    email: str
    password_hash: str

class User(BaseModel):
    id: int
    email: str
    disabled: bool = False
    password_hash: str

