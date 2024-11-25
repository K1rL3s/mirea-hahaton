from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

parse_settings = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)


class ApiConfig(BaseSettings):
    model_config = parse_settings

    port: int = Field(default=8000, alias="BACKEND_PORT")
    workers: int = Field(default=1, alias="BACKEND_WORKERS")


def get_api_config() -> ApiConfig:
    return ApiConfig()
