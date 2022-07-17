from enums import EnvEnum
from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    app_name: str = "Fast API Server"
    app_version: str = "0.0.1"
    app_env: EnvEnum = EnvEnum.DEV


class ModelSettings(BaseSettings):
    model_name_or_path: str = "/model"


server_settings = ServerSettings()
model_settings = ModelSettings()
