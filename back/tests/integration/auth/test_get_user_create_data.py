from httpx import AsyncClient
import pytest
from fakeredis.aioredis import FakeRedis
from src.api.utils.depends import RedisDep, redis_helper
from src.main import app
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.rabbit.email import router, email_publisher, SimpleTask
from src.config import config
from faststream.rabbit import TestRabbitBroker


@pytest.mark.asyncio
async def test_sign_up_send_data_succes(
        async_client: AsyncClient, fake_redis: FakeRedis
):
    @router.subscriber(config.rabbit.RABBIT_EMAIL_QUEUE)
    def subscriber(msg: dict):
        pass

    async with TestRabbitBroker(router.broker):
        app.dependency_overrides[redis_helper.get_redis] = lambda: fake_redis

        email = "test@example.com"
        password = "VeryStrongPass123!"

        payload = {"email": email, "password": password}
        response = await async_client.post("/auth/sign_up/send_data", json=payload)

        assert response.status_code == 200
        subscriber.mock.assert_called_once()


        app.dependency_overrides.clear()
