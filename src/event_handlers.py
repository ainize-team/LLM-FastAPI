from typing import Callable

from celery import Celery
from fastapi import FastAPI
from loguru import logger
from redis import Redis

from config import celery_settings, redis_settings


def _setup_redis(app: FastAPI) -> None:
    logger.info("Setup Redis")
    app.state.redis = Redis(
        host=redis_settings.redis_host,
        port=redis_settings.redis_port,
        db=redis_settings.redis_db,
        password=redis_settings.redis_password,
    )


def _setup_celery(app: FastAPI) -> None:
    logger.info("Setup Celery")
    celery_settings.backend_uri = "redis://:{password}@{hostname}:{port}/{db}".format(
        hostname=redis_settings.redis_host,
        password=redis_settings.redis_password,
        port=redis_settings.redis_port,
        db=redis_settings.redis_db,
    )
    app.state.celery = Celery(
        broker=celery_settings.broker_uri,
        backend=celery_settings.backend_uri,
    )


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running App Start Handler.")
        _setup_redis(app)
        _setup_celery(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running App Shutdown Handler.")
        del app.state.celery
        del app.state.redis

    return shutdown
