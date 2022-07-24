from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class CeleryWorkerSettings(BaseSettings):
    WORKER_NAME: str = "Celery Worker"
    BROKER_URI: str = ""
    BACKEND_URI: str = ""

    class Config:
        env_file = ".env"


class ModelSettings(BaseSettings):
    MODEL_PATH: str = ""
    USE_FAST_TOKENIZER: bool = True
    MODEL_MAX_LENGTH: int = 2048

    class Config:
        env_file = ".env"


celery_worker_settings = CeleryWorkerSettings()
model_settings = ModelSettings()
