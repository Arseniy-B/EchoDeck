from datetime import datetime
from pydantic import BaseModel


class Card(BaseModel):
    id: int
    deck_id: int
    question: str
    answer: str
    description: str

    created_at: datetime
    updated_at: datetime


class GhostCard(BaseModel):
    deck_id: int
    question: str
    answer: str
    description: str

    created_at: datetime
    updated_at: datetime


class CardCreateData(BaseModel):
    deck_id: int
    question: str
    answer: str
    description: str


class CardCreate(BaseModel):
    deck_id: int
    question: str
    answer: str
    description: str

    created_at: datetime
    updated_at: datetime


class CardOut(BaseModel):
    deck_id: int
    question: str
    answer: str
    description: str

    created_at: datetime
    updated_at: datetime

