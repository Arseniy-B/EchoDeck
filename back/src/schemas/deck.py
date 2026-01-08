from pydantic import BaseModel



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


class DeckOut(BaseModel):
    id: int
    title: str
    tracking_status: TrackingStatus
