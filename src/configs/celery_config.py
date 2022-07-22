from pydantic import BaseSettings


class CeleryWorkerSettings(BaseSettings):
    worker_name: str = "Celery Worker"
    broker_uri: str = ""
    backend_uri: str = ""


celery_worker_settings = CeleryWorkerSettings()
