# ServingLLMFastCelery

Serving Large Language Model Using FastAPI and Celery

## How to Server
1. Download LLM from huggingface and store it to your local storage.

2. build docker file
```
git clone https://github.com/ainize-team/ServingLLMFastCelery.git
cd ServingLLMFastCelery
docker build -t fastapi-llm .
```

3. run docker image
```
docker run -d --name bloom-serving -p 8000:8000 --gpus='"device=0,1,2,3,4,5,6,7"' -v <local_storage_path>:/model fastapi-llm
```

## For Developers

1. install dev package.

```shell
pip install -r requirements-dev.txt
```

2. install pre-commit.

```shell
pre-commit install
```
