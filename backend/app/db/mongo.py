from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

RAW_API_RESPONSES_COLLECTION = "raw_api_responses"
RAW_WEBHOOK_PAYLOADS_COLLECTION = "raw_webhook_payloads"
RAW_FILE_IMPORTS_COLLECTION = "raw_file_imports"
RAW_SCRAPED_PAGES_COLLECTION = "raw_scraped_pages"
RAW_CRYPTO_TRANSACTIONS_COLLECTION = "raw_crypto_transactions"

_mongo_client: AsyncIOMotorClient | None = None


def init_mongo_client() -> AsyncIOMotorClient:
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(settings.resolved_mongo_url)
    return _mongo_client


def get_mongo_client() -> AsyncIOMotorClient:
    if _mongo_client is None:
        return init_mongo_client()
    return _mongo_client


def get_mongo_database() -> AsyncIOMotorDatabase:
    return get_mongo_client()[settings.mongo_db]


async def check_mongo_health() -> None:
    database = get_mongo_database()
    await database.command("ping")


async def close_mongo_client() -> None:
    global _mongo_client
    if _mongo_client is not None:
        _mongo_client.close()
        _mongo_client = None

