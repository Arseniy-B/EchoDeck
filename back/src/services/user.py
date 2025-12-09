from sqlalchemy import select
from src.models.db import AsyncSession
from src.models.models import User
from src.schemas.user import User as UserSchema, UserCreate


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str) -> UserSchema:
        stmt = select(User).where(User.name == username)
        ans = await self.session.execute(stmt)
        user_model: User = ans.scalar_one()
        return UserSchema.model_validate(user_model.__dict__)

    async def add_new_user(self, user: UserCreate):
        self.session.add(User(**user.__dict__))
        await self.session.commit()
