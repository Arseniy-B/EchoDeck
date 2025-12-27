from pydantic import BaseModel
from src.models.models import TrackingStatus


class Deck(BaseModel):
    id: int
    user_id: int
    title: str
    tracking_status: TrackingStatus


class GhostDeck(BaseModel):
    user_id: int
    title: str
    tracking_status: TrackingStatus


class DeckCreateData(BaseModel):
    title: str
    tracking_status: TrackingStatus


class DeckCreate(BaseModel):
    user_id: int
    title: str
    tracking_status: TrackingStatus

