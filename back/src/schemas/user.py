from pydantic import BaseModel, EmailStr


class EmailUserLogin(BaseModel):
    email: EmailStr
    otp: str

class PasswordUserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class GhostUser(BaseModel):
    email: EmailStr
    disabled: bool = False
    password_hash: str

class User(BaseModel):
    id: int
    email: EmailStr
    disabled: bool = False
    password_hash: str

