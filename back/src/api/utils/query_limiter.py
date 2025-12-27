from functools import wraps
from fastapi.exceptions import HTTPException
from fastapi import status, Request
from src.api.utils.depends import RedisDep
from src.services.redis.keys import RedisKeys


async def email_query_limiter(request: Request, redis: RedisDep):
    body = await request.json()
    limit_key = body.get("email")

    if not limit_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email not found in request",
        )

    redis_key = RedisKeys.REQUEST_LIMITER.format(key=limit_key)
    count = await redis.incr(redis_key)

    if count == 1:
        await redis.expire(redis_key, 60)
    if count > 5:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Rate limit exceeded")
