from sqlalchemy import select
from src.models.db import AsyncSession
from src.models.models import User
from src.schemas.user import User as UserSchema, GhostUser
from src.services.crud import CRUD



class UserRepo(CRUD):
    async def get_user_by_email(self, email: str) -> UserSchema:
        stmt = select(User).where(User.email == email)
        ans = await self.session.execute(stmt)
        user_model: User = ans.scalar_one()
        return UserSchema.model_validate(user_model.__dict__)
