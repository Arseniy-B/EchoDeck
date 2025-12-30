from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select

from src.models.db import AsyncSession
from src.models.models import Base

T_Model = TypeVar("T_Model", bound=Base)

T_Schema = TypeVar("T_Schema", bound=BaseModel)
T_GhostSchema = TypeVar("T_GhostSchema", bound=BaseModel)
T_SchemaCreate = TypeVar("T_SchemaCreate", bound=BaseModel)
T_SchemaUpdate = TypeVar("T_SchemaUpdate", bound=BaseModel)


class CRUD(Generic[T_Model, T_Schema, T_GhostSchema, T_SchemaCreate, T_SchemaUpdate]):
    def __init__(
        self,
        session: AsyncSession,
        model: type[T_Model],
        schema: T_Schema,
        ghost_schema: T_GhostSchema, 
        schema_create: T_SchemaCreate,
    ):
        self.session = session
        self.model = model
        self.schema = schema
        self.ghost_schema = ghost_schema
        self.schema_create = schema_create

    async def get_by_id(self, id: int) -> T_Schema:
        stmt = select(self.model).where(self.model.id == id)
        exec_ans = await self.session.execute(stmt)
        ans: T_Model = exec_ans.scalar_one()
        return self.schema.model_validate(ans.__dict__)

    async def create(self, create_schema: T_SchemaCreate):
        obj = self.model(**create_schema.model_dump(exclude_unset=True))
        self.session.add(obj)
        await self.session.commit()

    async def update(self, update_schema: T_SchemaUpdate):
        db_obj = await self.session.get(self.model, id)
        if not db_obj:
            return None

        update_data = update_schema.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        await self.session.commit()
        return self.schema.model_validate(db_obj)

    async def delete(self, obj_id: int):
        obj = await self.session.get(self.model, obj_id)
        await self.session.delete(obj)
        await self.session.commit()
