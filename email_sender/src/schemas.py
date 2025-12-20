from pydantic import BaseModel, EmailStr


class SimpleTask(BaseModel):
    to: EmailStr
    payload: dict
    text_name: str

