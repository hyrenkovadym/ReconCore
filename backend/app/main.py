from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="ReconCore reconciliation and data quality platform API.",
    version="0.1.0",
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

