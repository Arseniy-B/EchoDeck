import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fakeredis.aioredis import FakeRedis
from src.services.redis.redis import redis_helper
from src.main import app
from src.services.rabbit.email import router
from src.config import config
from faststream.rabbit import TestRabbitBroker




@pytest_asyncio.fixture
async def mock_subscriber():
    @router.subscriber(config.rabbit.RABBIT_EMAIL_QUEUE)
    def subscriber(msg: dict):
        pass
    yield subscriber


@pytest_asyncio.fixture
async def setup_email_faststream(mock_subscriber):
    async with TestRabbitBroker(router.broker):
        yield mock_subscriber


@pytest_asyncio.fixture
async def fake_redis():
    redis = FakeRedis(async_mode=True, decode_responses=True)
    yield redis
    await redis.flushall()
    await redis.aclose()


@pytest_asyncio.fixture
async def setup_redis(fake_redis: FakeRedis):
    app.dependency_overrides[redis_helper.get_redis] = lambda: fake_redis
    yield fake_redis
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
