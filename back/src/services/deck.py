from src.services.crud import CRUD
from sqlalchemy import select
from src.schemas.deck import Deck
from src.models.models import Deck as DeckModel
from typing import Sequence


class DeckRepo(CRUD):
    async def get_all(self, user_id: int) -> list[Deck]:
        stmt = select(DeckModel).where(DeckModel.user_id == user_id)
        ans = await self.session.execute(stmt)
        deck_objs = ans.scalars().all()
        return [Deck.model_validate(i, from_attributes=True) for i in deck_objs]
