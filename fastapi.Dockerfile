FROM python:3.8.13-slim-buster

WORKDIR /app
COPY ./src/ ./
COPY requirements-fastapi.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "0"]