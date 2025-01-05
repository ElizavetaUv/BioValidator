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


class ObjectStore(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=CONFIG_FILE)

    BUCKET_NAME: str
    AWS_ACCESS_KEY_ID: SecretStr
    AWS_SECRET_ACCESS_KEY: SecretStr
    CUSTOM_S3_URL: str | None = Field(default=None)


class ReferenceDataConfig(BaseSettings):
    reference_dir: str = '../data/test_maf_output'


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=CONFIG_FILE)

    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    object_store: ObjectStore = Field(default_factory=ObjectStore)
    reference_data: ReferenceDataConfig = Field(default_factory=ReferenceDataConfig)


def get_config() -> Config:
    config = Config(_env_file=CONFIG_FILE)
    return config
