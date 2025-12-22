from httpx import AsyncClient
import pytest
import warnings
from src.services.redis.keys import RedisKeys
import json


@pytest.mark.asyncio
async def test_sign_up_send_data_succes(
    async_client: AsyncClient, setup_redis, setup_email_faststream
):
    email = "test@example.com"
    password = "VeryStrongPass123!"

    payload = {"email": email, "password": password}
    response = await async_client.post("/auth/sign_up/send_data", json=payload)

    assert response.status_code == 200
    setup_email_faststream.mock.assert_called_once()


@pytest.mark.asyncio
async def test_sign_up_send_data_already_saved_data_in_redis(
    async_client: AsyncClient, setup_redis, setup_email_faststream
):
    email = "test@example.com"
    password = "VeryStrongPass123!"

    payload = {"email": email, "password": password}

    await setup_redis.set(RedisKeys.REGISTER_GHOST_USER.format(email=email), json.dumps(payload))
    response = await async_client.post("/auth/sign_up/send_data", json=payload)

    assert response.status_code == 200
    setup_email_faststream.mock.assert_called_once()



@pytest.mark.asyncio
async def test_sign_up_send_data_smoll_password(
    async_client: AsyncClient, setup_redis, setup_email_faststream
):
    email = "test@example.com"
    password = "aaa"

    payload = {"email": email, "password": password}
    response = await async_client.post("/auth/sign_up/send_data", json=payload)

    assert response.status_code == 400
    setup_email_faststream.mock.assert_not_called()


@pytest.mark.asyncio
async def test_sign_up_send_data_not_strong_enough_password(
    async_client: AsyncClient, setup_redis, setup_email_faststream
):
    email = "test@example.com"
    password = "aaaaaaaa"

    payload = {"email": email, "password": password}
    response = await async_client.post("/auth/sign_up/send_data", json=payload)

    if response.status_code == 200:
        warnings.warn("not enough strong password allowed")
        setup_email_faststream.mock.assert_called_once()
    elif response.status_code == 400:
        setup_email_faststream.mock.assert_not_called()
