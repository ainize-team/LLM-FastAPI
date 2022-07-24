from fastapi import FastAPI

from enums import EnvEnum

from .configs.config import server_settings
from .event_handlers import start_app_handler, stop_app_handler
from .router import prediction


def get_app() -> FastAPI:
    fast_api_app = FastAPI(
        title=server_settings.APP_NAME,
        version=server_settings.APP_VERSION,
        debug=server_settings.APP_ENV == EnvEnum.DEV,
    )
    fast_api_app.include_router(prediction.router, tags=["prediction"])
    fast_api_app.add_event_handler("startup", start_app_handler(fast_api_app))
    fast_api_app.add_event_handler("shutdown", stop_app_handler(fast_api_app))
    return fast_api_app


app = get_app()
