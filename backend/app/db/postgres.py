from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings


engine: AsyncEngine = create_async_engine(
    settings.resolved_database_url,
    echo=settings.app_env == "development",
    pool_pre_ping=True,
    pool_recycle=1800,
)


async def check_postgres_health() -> None:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

