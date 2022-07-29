FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-devel

WORKDIR /app
COPY ./src/celery_tasks/ ./celery_tasks/
COPY requirements-celery.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["celery", "-A", "celery_tasks.worker", "worker", "--loglevel==info", "--pool=solo"]