from pydantic import BaseSettings

from .enums import EnvEnum


class ServerSettings(BaseSettings):
    app_name: str = "Fast API Server"
    app_version: str = "0.0.1"
    app_env: EnvEnum = EnvEnum.DEV


class ModelSettings(BaseSettings):
    model_max_length: int = 2048


class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""


class CelerySettings(BaseSettings):
    backend_uri: str = "setup"
    broker_uri: str


server_settings = ServerSettings()
model_settings = ModelSettings()
redis_settings = RedisSettings()
celery_settings = CelerySettings()
