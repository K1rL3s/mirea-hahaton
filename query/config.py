from pydantic import NatsDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

_parse_settings = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)


class NatsConfig(BaseSettings):
    model_config = _parse_settings

    nats_url: NatsDsn


def get_nats_config() -> NatsConfig:
    return NatsConfig()
