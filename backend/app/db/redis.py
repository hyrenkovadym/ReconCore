from redis.asyncio import Redis

from app.core.config import settings

# Redis will back cache, distributed locks, rate limiting, and temporary job states.
_redis_client: Redis | None = None


def init_redis_client() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(
            settings.resolved_redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


def get_redis_client() -> Redis:
    if _redis_client is None:
        return init_redis_client()
    return _redis_client


async def check_redis_health() -> None:
    redis_client = get_redis_client()
    await redis_client.ping()


async def close_redis_client() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None

