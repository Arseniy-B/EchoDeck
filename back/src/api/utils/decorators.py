from functools import wraps
from fastapi.exceptions import HTTPException
from fastapi import status, Request
from src.api.utils.depends import RedisDep
from src.services.redis.keys import RedisKeys


def query_limiter(field: str, rate_limit_per_minute: int = 5):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request, redis: RedisDep, **kwargs):
            body = await request.json()
            limit_key = body.get(field)
            
            if not limit_key:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{field} not found in request")

            redis_key = RedisKeys.REQUEST_LIMITER.format(key=limit_key)
            count = await redis.incr(redis_key)

            if count == 1:
                await redis.expire(redis_key, 60)
            if count > rate_limit_per_minute:
                raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Rate limit exceeded")

            ans = await func(*args, **kwargs)

            return ans
        return wrapper
    return decorator
