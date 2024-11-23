from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

parse_settings = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)


class SchedulerConfig(BaseSettings):
    model_config = parse_settings

    delay: int = Field(default=1)


def get_scheduler_config() -> SchedulerConfig:
    return SchedulerConfig()
