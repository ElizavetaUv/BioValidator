from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

_ENV_DEV_PATH = os.path.join(os.path.dirname(__file__), ".env-dev")
_ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")

class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=(_ENV_PATH, _ENV_DEV_PATH))

    POSTGRES_USER: str  
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: str = Field(default="5432")
    

class ReferenceDataConfig(BaseSettings):
    reference_dir: str = '../data/test_maf_output'


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=(_ENV_PATH, _ENV_DEV_PATH))

    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    reference_data: ReferenceDataConfig = Field(default_factory=ReferenceDataConfig)


def get_config() -> Config:
    config = Config(_env_file=(_ENV_PATH, _ENV_DEV_PATH))
    return config
