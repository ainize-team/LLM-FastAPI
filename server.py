from fastapi import FastAPI

from config import server_settings
from enums import EnvEnum
from event_handlers import start_app_handler


def get_app() -> FastAPI:
    fast_api_app = FastAPI(
        title=server_settings.app_name,
        version=server_settings.app_version,
        debug=server_settings.app_env == EnvEnum.DEV,
    )
    fast_api_app.add_event_handler("startup", start_app_handler(fast_api_app))
    return fast_api_app


app = get_app()
