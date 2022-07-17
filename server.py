from fastapi import FastAPI

from config import server_settings
from enums import EnvEnum


def get_app() -> FastAPI:
    fast_api_app = FastAPI(
        title=server_settings.app_name,
        version=server_settings.app_version,
        debug=server_settings.app_env == EnvEnum.DEV,
    )
    return fast_api_app


app = get_app()
