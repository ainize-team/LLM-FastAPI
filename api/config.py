from pydantic import BaseSettings, Field

from .enums import EnvEnum


class ServerSettings(BaseSettings):
    app_name: str = "Fast API Server"
    app_version: str = "0.0.1"
    app_env: EnvEnum = EnvEnum.DEV


class ModelSettings(BaseSettings):
    model_max_length: int = 2048


class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = Field(
        default=6379,
        ge=0,
        le=65535,
    )
    redis_db: int = Field(
        default=0,
        ge=0,
        le=15,
    )
    redis_password: str = ""


class CelerySettings(BaseSettings):
    backend_uri: str = "Auto Generate"
    broker_uri: str


server_settings = ServerSettings()
model_settings = ModelSettings()
redis_settings = RedisSettings()
celery_settings = CelerySettings()
