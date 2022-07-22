from fastapi import FastAPI

from api import prediction
from config import server_settings
from enums import EnvEnum
from event_handlers import start_app_handler, stop_app_handler


def get_app() -> FastAPI:
    fast_api_app = FastAPI(
        title=server_settings.app_name,
        version=server_settings.app_version,
        debug=server_settings.app_env == EnvEnum.DEV,
    )
    fast_api_app.include_router(prediction.router, tags=["prediction"])
    fast_api_app.add_event_handler("startup", start_app_handler(fast_api_app))
    fast_api_app.add_event_handler("shutdown", stop_app_handler(fast_api_app))
    return fast_api_app


app = get_app()
