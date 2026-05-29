import re

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.db.mongo import check_mongo_health
from app.db.postgres import check_postgres_health
from app.db.redis import check_redis_health


router = APIRouter()


def _safe_error_message(exc: Exception) -> str:
    raw_message = str(exc)
    sanitized = re.sub(r"://[^:@/]+:[^@/]+@", "://***:***@", raw_message)
    if sanitized:
        return f"{exc.__class__.__name__}: {sanitized}"
    return exc.__class__.__name__


@router.get("/")
async def healthcheck() -> dict[str, object] | JSONResponse:
    services: dict[str, str] = {
        "api": "ok",
        "postgres": "ok",
        "mongo": "ok",
        "redis": "ok",
    }
    errors: dict[str, str] = {}

    checks = (
        ("postgres", check_postgres_health),
        ("mongo", check_mongo_health),
        ("redis", check_redis_health),
    )

    for service_name, check_fn in checks:
        try:
            await check_fn()
        except Exception as exc:  # noqa: BLE001
            services[service_name] = "error"
            errors[service_name] = _safe_error_message(exc)

    if errors:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "services": services,
                "errors": errors,
            },
        )

    return {
        "status": "ok",
        "services": services,
    }
