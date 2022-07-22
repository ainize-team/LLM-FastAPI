from pydantic import BaseSettings


class CeleryWorkerSettings(BaseSettings):
    WORKER_NAME: str = "Celery Worker"
    BROKER_URI: str = ""
    BACKEND_URI: str = ""

    class Config:
        env_file = ".env"


celery_worker_settings = CeleryWorkerSettings()
