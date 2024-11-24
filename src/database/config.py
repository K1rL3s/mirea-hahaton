from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

_parse_settings = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)


class DBConfig(BaseSettings):
    model_config = _parse_settings

    db_url: PostgresDsn


def get_db_config() -> DBConfig:
    return DBConfig()
