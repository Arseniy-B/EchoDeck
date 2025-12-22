from httpx import AsyncClient
import pytest
import warnings
from src.services.redis.keys import RedisKeys
from src.schemas.user import EmailUserLogin, GhostUser
from src.utils.password import PasswordHelper as ps
import json
from src.models.db import AsyncSession, db_helper
import pytest_asyncio
from src.main import app
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_async_session() -> AsyncSession:
    session = AsyncMock(spec=AsyncSession)

    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    session.add_all = MagicMock()
    session.delete = MagicMock()
    session.flush = AsyncMock()

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_result.scalar.return_value = None
    session.execute.return_value = mock_result

    return session


@pytest_asyncio.fixture
async def setup_db_session(mock_async_session):
    app.dependency_overrides[db_helper.get_session] = lambda: mock_async_session
    yield mock_async_session
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_finish_sign_up_succes(
    async_client: AsyncClient, setup_redis, setup_db_session
):
    email = "test@example.com"
    otp = "123456"
    password = "asdafadsf"
    password_hash = ps.hash_password(password)

    await setup_redis.set(
        RedisKeys.REGISTER_OTP.format(email=email), ps.hash_password(otp)
    )

    ghost_user_payload = GhostUser(email=email, password_hash=password_hash).model_dump()
    await setup_redis.set(
        RedisKeys.REGISTER_GHOST_USER.format(email=email), json.dumps(ghost_user_payload)
    )


    payload = EmailUserLogin(email=email, otp=otp).model_dump()
    response = await async_client.post("/auth/sign_up/confirm_email", json=payload)

    assert response.status_code == 200
    setup_db_session.add.assert_called_once()
    setup_db_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_finish_sign_up_success(
    async_client: AsyncClient, setup_redis, setup_db_session
):
    email = "test@example.com"
    otp = "123456"
    password = "StrongPass123!"
    password_hash = ps.hash_password(password)

    # Подготовка Redis
    ghost_user = GhostUser(email=email, password_hash=password_hash)
    await setup_redis.set(RedisKeys.REGISTER_OTP.format(email=email), ps.hash_password(otp))
    await setup_redis.set(RedisKeys.REGISTER_GHOST_USER.format(email=email), json.dumps(ghost_user.model_dump()))

    payload = EmailUserLogin(email=email, otp=otp).model_dump()
    response = await async_client.post("/auth/sign_up/confirm_email", json=payload)

    assert response.status_code == 200
    setup_db_session.add.assert_called_once()
    setup_db_session.commit.assert_awaited_once()
    # Проверяем, что данные удалены из Redis
    assert await setup_redis.get(RedisKeys.REGISTER_OTP.format(email=email)) is None
    assert await setup_redis.get(RedisKeys.REGISTER_GHOST_USER.format(email=email)) is None


@pytest.mark.asyncio
async def test_finish_sign_up_wrong_otp(
    async_client: AsyncClient, setup_redis, setup_db_session
):
    email = "test@example.com"
    otp_correct = "123456"
    otp_wrong = "999999"
    password_hash = ps.hash_password("StrongPass123!")

    ghost_user = GhostUser(email=email, password_hash=password_hash)
    await setup_redis.set(RedisKeys.REGISTER_OTP.format(email=email), ps.hash_password(otp_correct))
    await setup_redis.set(RedisKeys.REGISTER_GHOST_USER.format(email=email), json.dumps(ghost_user.model_dump()))

    payload = EmailUserLogin(email=email, otp=otp_wrong).model_dump()
    response = await async_client.post("/auth/sign_up/confirm_email", json=payload)

    assert response.status_code in (400, 401)  # Зависит от твоей реализации ошибки
    setup_db_session.add.assert_not_called()
    setup_db_session.commit.assert_not_awaited()
    # Данные в Redis остаются
    assert await setup_redis.get(RedisKeys.REGISTER_OTP.format(email=email)) is not None


@pytest.mark.asyncio
async def test_finish_sign_up_otp_not_exists(
    async_client: AsyncClient, setup_redis, setup_db_session
):
    email = "test@example.com"
    password_hash = ps.hash_password("StrongPass123!")

    ghost_user = GhostUser(email=email, password_hash=password_hash)
    await setup_redis.set(RedisKeys.REGISTER_GHOST_USER.format(email=email), json.dumps(ghost_user.model_dump()))
    # OTP намеренно НЕ устанавливаем

    payload = EmailUserLogin(email=email, otp="123456").model_dump()
    response = await async_client.post("/auth/sign_up/confirm_email", json=payload)

    assert response.status_code in (400, 401)
    setup_db_session.add.assert_not_called()


@pytest.mark.asyncio
async def test_finish_sign_up_ghost_user_not_exists(
    async_client: AsyncClient, setup_redis, setup_db_session
):
    email = "unknown@example.com"
    otp = "123456"

    # Ничего не кладём в Redis
    payload = EmailUserLogin(email=email, otp=otp).model_dump()
    response = await async_client.post("/auth/sign_up/confirm_email", json=payload)

    assert response.status_code in (400, 404)
    setup_db_session.add.assert_not_called()


@pytest.mark.asyncio
async def test_finish_sign_up_invalid_email_format(
    async_client: AsyncClient, setup_redis, setup_db_session
):
    payload = {"email": "not-an-email", "otp": "123456"}
    response = await async_client.post("/auth/sign_up/confirm_email", json=payload)

    assert response.status_code == 422  # Pydantic validation error
    setup_db_session.add.assert_not_called()


@pytest.mark.asyncio
async def test_finish_sign_up_empty_fields(
    async_client: AsyncClient, setup_redis, setup_db_session
):
    payload = {"email": "", "otp": ""}
    response = await async_client.post("/auth/sign_up/confirm_email", json=payload)

    assert response.status_code == 422
    setup_db_session.add.assert_not_called()


@pytest.mark.asyncio
async def test_finish_sign_up_repeat_after_success(
    async_client: AsyncClient, setup_redis, setup_db_session
):
    # Сначала успешный запрос
    email = "repeat@example.com"
    otp = "123456"
    password_hash = ps.hash_password("Pass123!")

    ghost_user = GhostUser(email=email, password_hash=password_hash)
    await setup_redis.set(RedisKeys.REGISTER_OTP.format(email=email), ps.hash_password(otp))
    await setup_redis.set(RedisKeys.REGISTER_GHOST_USER.format(email=email), json.dumps(ghost_user.model_dump()))

    payload = EmailUserLogin(email=email, otp=otp).model_dump()
    response1 = await async_client.post("/auth/sign_up/confirm_email", json=payload)
    assert response1.status_code == 200
    setup_db_session.add.assert_called_once()  # Первый вызов

    # Повторный запрос с теми же данными
    setup_db_session.reset_mock()  # Сбрасываем моки для второго вызова
    response2 = await async_client.post("/auth/sign_up/confirm_email", json=payload)

    assert response2.status_code in (400, 404)  # Данные уже удалены
    setup_db_session.add.assert_not_called()
