from fastapi import Request, HTTPException
from redis import Redis
import os

redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)

RATE_LIMIT = 10          # requests
RATE_LIMIT_WINDOW = 60   # seconds


async def rate_limiter(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    current = redis_client.get(key)

    if current and int(current) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Slow down."
        )

    pipe = redis_client.pipeline()
    pipe.incr(key, 1)

    if not current:
        pipe.expire(key, RATE_LIMIT_WINDOW)

    pipe.execute()