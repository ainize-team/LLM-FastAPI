from celery import Celery

from configs.celery_config import celery_worker_settings


app = Celery(
    celery_worker_settings.worker_name,
    broker=celery_worker_settings.broker_uri,
    backend=celery_worker_settings.backend_uri,
    include=["celery_tasks.tasks"],
)
