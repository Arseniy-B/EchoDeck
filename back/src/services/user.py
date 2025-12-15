from sqlalchemy import select
from src.models.db import AsyncSession
from src.models.models import User
from src.schemas.user import User as UserSchema, GhostUser


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> UserSchema:
        stmt = select(User).where(User.email == email)
        ans = await self.session.execute(stmt)
        user_model: User = ans.scalar_one()
        return UserSchema.model_validate(user_model.__dict__)
    
    async def get_user_by_id(self, id: int) -> None | UserSchema: 
        stmt = select(User).where(User.id == id)
        ans = await self.session.execute(stmt)
        user_model: User = ans.scalar_one()
        return UserSchema.model_validate(user_model.__dict__)

    async def add_new_user(self, user: GhostUser):
        self.session.add(User(**user.__dict__))
        await self.session.commit()
