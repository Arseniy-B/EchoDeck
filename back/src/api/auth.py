import json
import logging

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from pydantic import EmailStr

from src.api.utils.depends import (
    AuthDep,
    RedisDep,
    UserRepoDep,
)
from src.config import config
from src.schemas.user import (
    EmailUserLogin,
    GhostUser,
    PasswordUserLogin,
    User,
    UserCreate,
)
from src.utils.otp import generate_otp_code
from src.utils.password import PasswordHelper as ps
from src.services.redis.keys import RedisKeys
from src.services.rabbit.email import email_publisher, SimpleTask, TEMPLATES


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth")


@router.post("/sign_up/send_data", response_model=None)
async def get_user_create_data(
    redis: RedisDep,
    user_create: UserCreate,
):
    if not ps.check_password_strength(user_create.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="password too weak"
        )
    password_hash = ps.hash_password(user_create.password)
    user = GhostUser(email=user_create.email, password_hash=password_hash)

    otp = generate_otp_code()
    print(otp)
    await redis.set(RedisKeys.REGISTER_OTP.format(email=user.email), ps.hash_password(otp))
    logger.info("OTP has been saved in redis", extra={"email": user_create.email})

    await redis.set(RedisKeys.REGISTER_GHOST_USER.format(email=user.email), json.dumps(user.model_dump()))
    logger.info(
        "ghost_user's data has been saved in redis", extra={"email": user_create.email}
    )

    task = SimpleTask(to=user.email, text_name=TEMPLATES.REGISTER_CONFIRM_EMAIL, payload={"otp": otp})
    await email_publisher(task)
    logger.info("a OTP has been sent to rebbitMQ", extra={"email": user_create.email})
    return {"success": "OK"}


@router.post("/sign_up/confirm_email")
async def finish_sign_up(
    redis: RedisDep,
    user_repo: UserRepoDep,
    user_login: EmailUserLogin,
    auth_repo: AuthDep
):
    otp_hash_redis_key = RedisKeys.REGISTER_OTP.format(email=user_login.email)
    otp_hash = await redis.get(otp_hash_redis_key)
    if not otp_hash or not ps.verify_password(user_login.otp, otp_hash):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    ghost_user_redis_key = RedisKeys.REGISTER_GHOST_USER.format(email=user_login.email)
    user_json = await redis.get(ghost_user_redis_key)
    if not user_json:
        logger.info(
            "Signup confirm failed: ghost user not found",
            extra={"email": user_login.email},
        )
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="sign up not started")
    user = GhostUser.model_validate(json.loads(user_json))
    await user_repo.add_new_user(user)

    await redis.delete(otp_hash_redis_key)
    await redis.delete(ghost_user_redis_key)
    logger.info("create user", extra={"email": user.email})
    auth_repo.login(user)



@router.post("/sign_in/send_otp")
async def send_otp_to_email(
    email: EmailStr, user_repo: UserRepoDep, redis: RedisDep
):
    user = await user_repo.get_user_by_email(email)
    if not user:
        logger.info(
            "attempt to log in to a non-existent account", extra={"email": user.email}
        )
        raise HTTPException(status.HTTP_200_OK)

    otp = generate_otp_code()
    await redis.set(RedisKeys.LOGIN_OTP.format(email=email), ps.hash_password(otp))
    task = SimpleTask(to=email, text_name=TEMPLATES.LOGIN_CONFIRM_EMAIL, payload={"otp": otp})
    await email_publisher(task)


@router.post("/sign_in/email")
async def login_by_email(
    auth_repo: AuthDep,
    user_repo: UserRepoDep,
    user_login: EmailUserLogin,
    redis: RedisDep
):
    otp_hash = await redis.get(RedisKeys.LOGIN_OTP.format(email=user_login.email))
    if not ps.verify_password(otp_hash, user_login.otp):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="incorrect credentials"
        )
    user = await user_repo.get_user_by_email(user_login.email)
    if not user:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="incorrect credentials"
        )
    auth_repo.login(user)


@router.post("/sign_in/password")
async def login_password(
    auth_repo: AuthDep, user_repo: UserRepoDep, user_login: PasswordUserLogin
):
    user = await user_repo.get_user_by_email(user_login.email)
    if not user or not ps.verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Incorrect username or password"
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
