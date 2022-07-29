from pydantic import BaseSettings

from ..enums import EnvEnum


class ServerSettings(BaseSettings):
    APP_NAME: str = "Fast API Server"
    APP_VERSION: str = "0.0.1"
    APP_ENV: EnvEnum = EnvEnum.DEV


class ModelSettings(BaseSettings):
    MODEL_PATH: str = "/model"
    USE_FAST_TOKENIZER: bool = True
    MODEL_MAX_LENGTH: int = 2048


server_settings = ServerSettings()
model_settings = ModelSettings()
