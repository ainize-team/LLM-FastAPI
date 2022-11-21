# LLM-FastAPI

Serving LLM(Large Language Model) Using FastAPI and Celery. This repository contains FastAPI server. If you want to see celery worker code, refer to [LLM-Worker](https://github.com/ainize-team/LLM-Worker) repository

## How to Run

1. run celery worker

- How to run celery worker is in [LLM-Worker](https://github.com/ainize-team/LLM-Worker) repository.

2. build docker file

```shell
git clone https://github.com/ainize-team/LLM-FastAPI.git
cd LLM-FastAPI
docker build -t llm-fastapi .
```

3. run docker image

- **Environment Variable**

  - `APP_NAME`= default : "FastAPI Server"
  - `REDIS_HOST`= default : "localhost"
  - `REDIS_PORT`= default : 6379
  - `REDIS_DB`= default : 0
  - `REDIS_PASSWORD`= default : ""
  - `BROKER_URI`= **Required**
  - `NUMBER_OF_WORKERS`= default : # of CPU cores

- You must use same following `broker_uri` and `backend_uri` to connect to celery worker
  - RabbitMQ broker uri: `ampq://<user>:<password>@<hostname>:<port>/<vhost>`
  - Redis backend uri: `redis://:<password>@<hostname>:<port>/<db>`
- If you use this code in linux and same sequence of this docs, maybe hostname is `172.17.0.1`, in macOS, `host.docker.internal`

  ```shell
  docker run -d --name <fastapi_container_name> -p <port>:8000 \
  -e APP_NAME=<app_name> -e BROKER_URI=<broker_uri> \
  -e REDIS_HOST=<redis_hostname> -e REDIS_PORT=<redis_port> \
  -e REDIS_DB=<redis_db> -e REDIS_PASSWORD=<redis_password> \
  -e NUMBER_OF_WORKERS=<num> llm-fastapi
  ```

  Or you can use the [.env file](./.env.sample) to run as follows.

  ```shell
  docker run -d --name <fastapi_container_name> -p <port>:8000 \
  --env-file <env_file_path> llm-fastapi
  ```

## How to Test

You can test the server when celery worker run together.

### Use curl

1. Request by POST with prompt

```
curl --location --request POST "http://localhost:<port>/generate" --header "Content-Type: application/json" --data-raw '{"prompt": "My name is"}'
```

- This will return `task_id`

2. Get results using task id

```
curl -X GET "http://localhost:<port>/result/<task_id>"
```

- This will return `status` with `result`
- Possible types of `status`

  ```python
  # src/enums.py
  class ResponseStatusEnum(StrEnum):
      PENDING: str = "pending"
      ASSIGNED: str = "assigned"
      COMPLETED: str = "completed"
      ERROR: str = "error"
  ```

- If status is `"assigned"`, the task is in progress. try again later.

### Swagger API Docs

- Check `http://localhost:<port>/docs` and `http://localhost:<port>/redoc`
  - In `docs`, you can test this easily.
  - In `redoc`, you can check request form.

## Test example

```
$ curl --location --request POST "http://localhost:8000/generate" --header "Content-Type: application/json" --data-raw '{"prompt": "My name is"}'
{"task_id":"f1c11ed3-6b32-4ecb-9f53-c0b1910d8fcf"}

$ curl -X GET "http://localhost:8000/result/f1c11ed3-6b32-4ecb-9f53-c0b1910d8fcf"
{"status":"completed","result":["My name is not spelled correctly in the list.\nMy apologies, I have fixed it :"]}
```

## For Developers

### 1. install dev package.

```shell
poetry install
```

### 2. install pre-commit.

```shell
pre-commit install
```
