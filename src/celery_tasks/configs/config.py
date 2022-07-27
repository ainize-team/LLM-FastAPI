from pydantic import BaseSettings


class CeleryWorkerSettings(BaseSettings):
    worker_name: str = "Celery Worker"
    broker_uri: str
    backend_uri: str


class ModelSettings(BaseSettings):
    model_path: str
    use_fast_tokenizer: bool = True
    model_max_length: int = 2048


celery_worker_settings = CeleryWorkerSettings()
model_settings = ModelSettings()
