from src.services.crud import CRUD
from sqlalchemy import select, insert, literal
from src.models.models import (
    Card as CardModel,
    Note as NoteModel,
    Deck as DeckModel,
    Collection as CollectionModel,
)
from datetime import datetime
from src.models.db import AsyncSession


class Schedule:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_to_learn(self, user_id: int, collection_id: int):
        deck = DeckModel(user_id=user_id)
        self.session.add(deck)
        await self.session.flush()

        subq = (
            select(NoteModel).where(NoteModel.collection_id == collection_id).scalar_subquery()
        )

        stmt = insert(CardModel).from_select(
            [
                CardModel.deck_id,
                CardModel.note_id,
                CardModel.last_repeat,
                CardModel.ease_factor,
            ],
            select(literal(deck.id), subq, literal(datetime.now()), literal(2500)))

        await self.session.execute(stmt)
        await self.session.commit()
