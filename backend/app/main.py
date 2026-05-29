from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.db.mongo import close_mongo_client, init_mongo_client
from app.db.postgres import engine
from app.db.redis import close_redis_client, init_redis_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_mongo_client()
    init_redis_client()
    yield
    await close_redis_client()
    await close_mongo_client()
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description="ReconCore reconciliation and data quality platform API.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    return {"service": settings.app_name, "status": "ok"}


app.include_router(api_v1_router, prefix="/api/v1")
