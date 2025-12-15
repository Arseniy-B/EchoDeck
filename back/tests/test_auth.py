from inspect import trace
import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app

@pytest.mark.asyncio
async def test_func():
    async with AsyncClient(transport=ASGITransport(app=app)) as ac:
        await ac.get("")
