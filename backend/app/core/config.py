from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="ReconCore API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    postgres_db: str = Field(default="reconcore", alias="POSTGRES_DB")
    postgres_user: str = Field(default="reconcore", alias="POSTGRES_USER")
    postgres_password: str = Field(default="reconcore", alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(default="postgres", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    database_url: str | None = Field(default=None, alias="DATABASE_URL")

    mongo_root_username: str = Field(default="reconcore", alias="MONGO_ROOT_USERNAME")
    mongo_root_password: str = Field(default="reconcore", alias="MONGO_ROOT_PASSWORD")
    mongo_host: str = Field(default="mongo", alias="MONGO_HOST")
    mongo_port: int = Field(default=27017, alias="MONGO_PORT")
    mongo_db: str = Field(default="reconcore_raw", alias="MONGO_DB")
    mongo_url: str | None = Field(default=None, alias="MONGO_URL")

    redis_host: str = Field(default="redis", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_dsn: str | None = Field(default=None, alias="REDIS_URL")

    rabbitmq_default_user: str = Field(default="reconcore", alias="RABBITMQ_DEFAULT_USER")
    rabbitmq_default_pass: str = Field(default="reconcore", alias="RABBITMQ_DEFAULT_PASS")
    rabbitmq_host: str = Field(default="rabbitmq", alias="RABBITMQ_HOST")
    rabbitmq_port: int = Field(default=5672, alias="RABBITMQ_PORT")
    rabbitmq_url: str | None = Field(default=None, alias="RABBITMQ_URL")

    celery_broker_url: str | None = Field(default=None, alias="CELERY_BROKER_URL")
    celery_result_backend: str | None = Field(default=None, alias="CELERY_RESULT_BACKEND")

    aws_access_key_id: str | None = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")
    s3_bucket: str = Field(default="reconcore-dev-bucket", alias="S3_BUCKET")

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def resolved_mongo_url(self) -> str:
        if self.mongo_url:
            return self.mongo_url
        return (
            f"mongodb://{self.mongo_root_username}:{self.mongo_root_password}"
            f"@{self.mongo_host}:{self.mongo_port}/{self.mongo_db}?authSource=admin"
        )

    @property
    def resolved_redis_url(self) -> str:
        if self.redis_dsn:
            return self.redis_dsn
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def resolved_rabbitmq_url(self) -> str:
        if self.rabbitmq_url:
            return self.rabbitmq_url
        return (
            "amqp://"
            f"{self.rabbitmq_default_user}:{self.rabbitmq_default_pass}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}//"
        )

    @property
    def resolved_celery_broker_url(self) -> str:
        if self.celery_broker_url:
            return self.celery_broker_url
        return self.resolved_rabbitmq_url

    @property
    def resolved_celery_result_backend(self) -> str:
        if self.celery_result_backend:
            return self.celery_result_backend
        return self.resolved_redis_url

    @property
    def sqlalchemy_database_uri(self) -> str:
        return self.resolved_database_url

    @property
    def mongodb_uri(self) -> str:
        return self.resolved_mongo_url

    @property
    def redis_url(self) -> str:
        return self.resolved_redis_url


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
