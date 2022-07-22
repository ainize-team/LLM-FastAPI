from pydantic import BaseSettings

from enums import EnvEnum


class ServerSettings(BaseSettings):
    app_name: str = "Fast API Server"
    app_version: str = "0.0.1"
    app_env: EnvEnum = EnvEnum.DEV


class ModelSettings(BaseSettings):
    model_path: str = "/model"
    use_fast_tokenizer: bool = True
    model_max_length: int = 2048


server_settings = ServerSettings()
model_settings = ModelSettings()
