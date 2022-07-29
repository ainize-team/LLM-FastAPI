# LLM-FastAPI 
with Celery Worker

Serving Large Language Model Using FastAPI and Celery

## How to Server

### Celery Worker

1. Download LLM from huggingface and store it to your local storage.
2. Running RabbitMQ server using Docker
```
docker run -d --name rabbitmq -p 5672:5672 -p 8080:15672 --restart=unless-stopped rabbitmq:3.9.21-management
```

3. Running Redis using Docker
```
docker run --name redis -d -p 6379:6379 redis
```
- Want to control Redis
  - `sudo apt install redis-tools` in local shell


4. build docker file
```
git clone https://github.com/ainize-team/LLM-FastAPI.git
cd LLM-FastAPI
docker build -t celery-llm -f ./celery.Dockerfile .
docker build -t fastapi-llm -f ./fastapi.Dockerfile .
```

5. run docker image
```
docker run -d --name {worker_container_name} --gpus='"device=0,1,2,3,4,5,6,7"' -e USE_FAST_TOKENIZER=False -e BROKER_URI={broker_uri} -e BACKEND_URI={backend_uri} -v {local-path}:/model celery-llm

docker run -d --name {fastapi_container_name} -p {port}:8000 -e APP_NAME={app_name} -e BROKER_URI={broker_uri} -e BACKEND_URI={backend_uri} fastapi-llm
```

- Both containers must use same `broker_uri` and `backend_uri`
- **RabbitMQ broker uri**: `ampq://<user>:<password>@<hostname>:<port>/<vhost>`
- **Redis backend uri**: `redis://:<password>@<hostname>:<port>/<db>`
- If you use this code in linux and same sequence of this docs, maybe hostname is `172.17.0.1`, in macOS, `host.docker.internal`
- Radis port : 6379, RabbitMQ port : 5672

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
# src/api/enums.py
class ResponseStatusEnum(Enum):
    PENDING: str = "pending"
    COMPLETED: str = "completed"
```

- If status is `"pending"`, try again and again.

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
pip install -r requirements-dev.txt
```

### 2. install pre-commit.

```shell
pre-commit install
```