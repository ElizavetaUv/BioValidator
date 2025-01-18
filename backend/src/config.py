import os

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_FILE = os.getenv("CONFIG_FILE", ".env-dev")

# _ENV_DEV_PATH = os.path.join(os.path.dirname(__file__), ".env-dev")
# _ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")

class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=CONFIG_FILE)

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: str = Field(default="5432")


class RabbitmqConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=CONFIG_FILE)

    RABBITMQ_AMQP_PORT: str = Field(default="5672")
    RABBITMQ_HTTP_PORT: str = Field(default="15672")

    RABBITMQ_HOST: str
    RABBITMQ_PASSWORD: SecretStr
    RABBITMQ_USER: str
    RABBITMQ_VHOST: str

    def get_amqp_uri(self) -> str:
        creds = f"{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD.get_secret_value()}"
        location = f"{self.RABBITMQ_HOST}:{self.RABBITMQ_AMQP_PORT}"
        url = f"amqp://{creds}@{location}/{self.RABBITMQ_VHOST}?heartbeat=30&blocked_connection_timeout=60"
        return url


class WorkerConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=CONFIG_FILE)

    WORKER_MEMCACHED_HOST: str
    WORKER_MEMCACHED_PORT: str


class ObjectStore(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=CONFIG_FILE)

    BUCKET_NAME: str
    AWS_ACCESS_KEY_ID: SecretStr
    AWS_SECRET_ACCESS_KEY: SecretStr
    CUSTOM_S3_URL: str | None = Field(default=None)


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=CONFIG_FILE)

    LOG_LEVEL: str = Field(default="DEBUG")

    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    worker: WorkerConfig = Field(default_factory=WorkerConfig)
    rabbitmq: RabbitmqConfig = Field(default_factory=RabbitmqConfig)
    object_store: ObjectStore = Field(default_factory=ObjectStore)


def get_config() -> Config:
    config = Config(_env_file=CONFIG_FILE)
    return config
