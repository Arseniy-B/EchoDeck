from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from pydantic import EmailStr

from src.infrastructure.password import PasswordHelper as ps
from src.schemas.user import (
    GhostUser,
    User,
    UserCreate,
    EmailUserLogin,
    PasswordUserLogin,
)
from src.endpoints.depends import UserRepoDep, OtpStorageDep, RedisDep, AuthDep
from src.services.auth import get_email_ghost_user_key, send_otp, generate_otp_code
import json
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth")


@router.post("/sign_up/send_data")
async def get_user_create_data(
    otp_storage: OtpStorageDep, redis: RedisDep, user_create: UserCreate
):
    if not ps.check_password_strength(user_create.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="password too weak"
        )
    password_hash = ps.hash_password(user_create.password)
    user = GhostUser(email=user_create.email, password_hash=password_hash)
    await otp_storage.save_otp(user_create.email, generate_otp_code())
    logger.info("OTP has been saved in redis", extra={"email": user_create.email})

    redis.set(get_email_ghost_user_key(user.email), json.dumps(user.model_dump()))
    logger.info(
        "ghost_user's data has been saved in redis", extra={"email": user_create.email}
    )

    await send_otp(user_create.email)
    logger.info("a OTP has been sent to email", extra={"email": user_create.email})


@router.post("/sign_up/confirm_email")
async def finish_sign_up(
    otp_storage: OtpStorageDep,
    redis: RedisDep,
    user_repo: UserRepoDep,
    user_login: EmailUserLogin,
):
    await otp_storage.verify_otp(user_login.email, user_login.otp)
    user_json = await redis.get(get_email_ghost_user_key(user_login.email))
    if not user_json:
        logger.info(
            "Signup confirm failed: ghost user not found",
            extra={"email": user_login.email},
        )
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="sign up not started")
    user = GhostUser.model_validate(json.loads(user_json))
    await user_repo.add_new_user(user)
    logger.info("create user", extra={"email": user.email})


@router.post("/sign_in/send_otp")
async def send_otp_to_email(email: EmailStr, otp_storage: OtpStorageDep): 
    otp = generate_otp_code()
    await otp_storage.save_otp(email, otp)
    await send_otp(email)



@router.post("/sign_in/email")
async def login_by_email(
    auth_repo: AuthDep,
    user_repo: UserRepoDep,
    otp_storage: OtpStorageDep,
    user_login: EmailUserLogin,
):
    if not otp_storage.verify_otp(otp=user_login.otp, email=user_login.email):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="incorrect credentials"
        )
    user = await user_repo.get_user_by_email(user_login.email)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="incorrect credentials"
        )
    auth_repo.login(user)


@router.post("/sign_in/password")
async def login_password(
    auth_repo: AuthDep, user_repo: UserRepoDep, user_login: PasswordUserLogin
):
    user = await user_repo.get_user_by_email(user_login.email)
    if not user or not ps.verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password"
        )
    auth_repo.login(user)


@router.get("/token")
async def refresh_token(auth_repo: AuthDep, user_repo: UserRepoDep):
    refresh = auth_repo.get_refresh()
    if not refresh or auth_repo.verify_refresh(refresh):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="invalid or expired refresh token"
        )
    user_id = auth_repo.get_token_user_id(refresh)
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="invalid or expired refresh token"
        ) 
    auth_repo.refresh()
    logger.info("refresh token", extra={"email": user.email})
