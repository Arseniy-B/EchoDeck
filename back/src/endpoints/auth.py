from typing import Annotated
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status, Body
from src.services.user import add_new_user
from src.models.db import AsyncSession, db_helper
from src.schemas.user import User, UserCreate, GhostUser
from src.infrastructure.password import PasswordHelper as ps
from src.infrastructure.email import EmailSender

router = APIRouter(prefix="/auth")

SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]


@router.post("/sign_up/send_data")
async def get_user_create_data(session: SessionDep, user_create: UserCreate):
    if not ps.check_password_strength(user_create.password):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password too weak")
    password_hash = ps.hash_password(user_create.password)
    GhostUser(email=user_create.email, password_hash=password_hash)


@router.post("/sign_up/confirm_email")
async def finish_sign_up(code: int = Body()):
    ...

@router.post("/sign_up")
async def register(session: SessionDep, user_create: UserCreate):
    if not ps.check_password_strength(user_create.password):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password too weak")
    password_hash = ps.hash_password(user_create.password)
    
    await add_new_user(
        UserCreate.model_validate(
            {
                "name": user_create.email,
                "password_hash": password_hash,
                "disabled": False,
                "email": "!!!!!!",
            }
        ),
        session=session,
    )
    return {"success": True}

