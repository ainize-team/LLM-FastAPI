from pydantic import BaseSettings


class CeleryWorkerSettings(BaseSettings):
    worker_name: str = "Celery Worker"
    broker_uri: str
    backend_uri: str = ""


class ModelSettings(BaseSettings):
    model_path: str = "/model"
    use_fast_tokenizer: bool = True
    model_max_length: int = 2048


class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""


celery_worker_settings = CeleryWorkerSettings()
model_settings = ModelSettings()
redis_settings = RedisSettings()

celery_worker_settings.backend_uri = "redis://:{password}@{hostname}:{port}/{db}".format(
    hostname=redis_settings.redis_host,
    password=redis_settings.redis_password,
    port=redis_settings.redis_port,
    db=redis_settings.redis_db,
)
