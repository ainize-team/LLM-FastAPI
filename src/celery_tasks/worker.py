from celery import Celery

from configs.celery_config import celery_worker_settings


app = Celery(
    celery_worker_settings.WORKER_NAME,
    broker=celery_worker_settings.BROKER_URI,
    backend=celery_worker_settings.BACKEND_URI,
    include=["celery_tasks.tasks"],
)
