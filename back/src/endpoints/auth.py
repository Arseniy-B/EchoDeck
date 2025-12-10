from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException

from src.infrastructure.password import PasswordHelper as ps
from src.schemas.user import GhostUser, User, UserCreate, EmailUserLogin
from src.endpoints.depends import UserRepoDep, OtpStorageDep, RedisDep
from src.services.auth import get_email_ghost_user_key
import json


router = APIRouter(prefix="/auth")


@router.post("/sign_up/send_data")
async def get_user_create_data(
    otp_storage: OtpStorageDep, redis: RedisDep, user_create: UserCreate
):
    if not ps.check_password_strength(user_create.password):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="password too weak"
        )
    password_hash = ps.hash_password(user_create.password)
    user = GhostUser(email=user_create.email, password_hash=password_hash)
    await otp_storage.save_otp(user_create.email)
    redis.set(get_email_ghost_user_key(user.email), json.dumps(user.model_dump()))


@router.post("/sign_up/confirm_email")
async def finish_sign_up(
    otp_storage: OtpStorageDep,
    redis: RedisDep,
    user_repo: UserRepoDep,
    user_login: EmailUserLogin,
):
    await otp_storage.verify_otp(user_login.email, user_login.otp)
    user_json = await redis.get(get_email_ghost_user_key(user_login.email))
    user = GhostUser.model_validate(json.loads(user_json))
    await user_repo.add_new_user(user)
    return {"success": True}
