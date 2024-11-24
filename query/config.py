from pydantic import Field, NatsDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

_parse_settings = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)


class NatsConfig(BaseSettings):
    model_config = _parse_settings

    nats_url: NatsDsn
    workers: int = Field(default=1, alias="QUERY_WORKERS")


def get_nats_config() -> NatsConfig:
    return NatsConfig()
