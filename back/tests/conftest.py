import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from fakeredis.aioredis import FakeRedis
from unittest.mock import AsyncMock, patch
from src.main import app


@pytest_asyncio.fixture
async def fake_redis():
    redis = FakeRedis(async_mode=True, decode_responses=True)
    yield redis
    await redis.flushall()
    await redis.aclose()


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
