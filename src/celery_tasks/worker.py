import celeryconfig
from celery import Celery
from redis import Redis

from .config import celery_worker_settings, redis_settings


app = Celery(
    celery_worker_settings.worker_name,
    broker=celery_worker_settings.broker_uri,
    backend=celery_worker_settings.backend_uri,
    include=["celery_tasks.tasks"],
)
app.config_from_object(celeryconfig)
redis = Redis(
    host=redis_settings.redis_host,
    port=redis_settings.redis_port,
    db=redis_settings.redis_db,
    password=redis_settings.redis_password,
)
