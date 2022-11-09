# LLM-FastAPI

Serving Large Language Model Using FastAPI and Celery

## How to Server

### Celery Worker

- **Use Redis as backend and RabbitMQ as broker**

1. build docker file

```
git clone https://github.com/ainize-team/LLM-FastAPI.git
cd LLM-FastAPI
docker build -t fastapi-llm .
```

2. run docker image

- **Environment Variable**

  - `APP_NAME`= default : "FastAPI Server"
  - `REDIS_HOST`= default : "localhost"
  - `REDIS_PORT`= default : 6379
  - `REDIS_DB`= default : 0
  - `REDIS_PASSWORD`= default ""
  - `BROKER_URI`= **Required**
  - `NUMBER_OF_WORKERS`= default : NUM of CPU cores

- Must use same `broker_uri` and `backend_uri` with Worker
- **RabbitMQ broker uri**: `ampq://<user>:<password>@<hostname>:<port>/<vhost>`
- **Redis backend uri**: `redis://:<password>@<hostname>:<port>/<db>`
- If you use this code in linux and same sequence of this docs, maybe hostname is `172.17.0.1`, in macOS, `host.docker.internal`
- Radis port : 6379, RabbitMQ port : 5672

```
docker run -d --name {fastapi_container_name} -p {port}:8000
-e APP_NAME={app_name} -e BROKER_URI={broker_uri}
-e REDIS_HOST=<redis_hostname> -e REDIS_PORT=<redis_port>
-e REDIS_DB=<redis_db> -e REDIS_PASSWORD=<redis_password>
-e NUMBER_OF_WORKERS=<num> fastapi-llm
```

## How to Test

### Use curl

1. First, request by POST

```
curl --location --request POST "http://localhost:<port>/generate" --header "Content-Type: application/json" --data-raw '{"prompt": "My name is"}'
```

- This will return `task_id`

2. Next, request by GET

```
curl -X GET "http://localhost:8000/result/{task_id}"
```

- This will return `status` with `result`
- `status` is this

```python
# llm_fastapi/enums.py
class ResponseStatusEnum(StrEnum):
    PENDING: str = "pending"
    ASSIGNED: str = "assigned"
    COMPLETED: str = "completed"
    ERROR: str = "error"
```

- If status is `"assigned"`, try again and again.

### Use FastAPI docs

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
