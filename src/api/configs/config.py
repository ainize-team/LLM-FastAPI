from os.path import abspath, dirname, join

from dotenv import load_dotenv
from pydantic import BaseSettings

from ..enums import EnvEnum


BASE_DIR = dirname(abspath("./"))
load_dotenv(join(BASE_DIR, ".env"))


class ServerSettings(BaseSettings):
    APP_NAME: str = "Fast API Server"
    APP_VERSION: str = "0.0.1"
    APP_ENV: EnvEnum = EnvEnum.DEV

    class Config:
        env_file = ".env"


class ModelSettings(BaseSettings):
    MODEL_PATH: str
    USE_FAST_TOKENIZER: bool = True
    MODEL_MAX_LENGTH: int = 2048

    class Config:
        env_file = ".env"


server_settings = ServerSettings()
model_settings = ModelSettings()
