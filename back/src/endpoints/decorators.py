from functools import wraps
from src.infrastructure.redis import redis_helper, Redis
from datetime import datetime, timedelta
from fastapi.exceptions import HTTPException
from fastapi import status


DATE_FORMAT = "%Y-%m-%d %H:%M"
def REDIS_KEY(func_name, field): return f"{func_name}:{field}"

def query_limiter(seconds: int, field: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = await redis_helper.get_redis()
            last_query = await redis.get(REDIS_KEY(func.__name__, ))
            if last_query:
                datetime.strptime(last_query, DATE_FORMAT)
                if last_query + timedelta(0, seconds) > datetime.now():
                    return HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)
            ans = await func(*args, **kwargs)
            date = datetime.strftime(datetime.now(), DATE_FORMAT)
            redis.set(REDIS_KEY(func.__name__, ), date)
            return ans
        return wrapper
    return decorator
