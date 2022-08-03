import uuid
from datetime import datetime
from typing import Dict

import fastapi
import pytz
from celery import Celery
from fastapi import APIRouter, HTTPException, Request
from redis import Redis

from ..enums import ResponseStatusEnum
from ..payloads.request import TextGenerationRequest
from ..payloads.response import AsyncTaskResponse, TextGenerationResponse


router = APIRouter()


@router.post("/generate")
def post_generation(request: Request, data: TextGenerationRequest) -> AsyncTaskResponse:
    redis: Redis = request.app.state.redis
    celery: Celery = request.app.state.celery
    now = datetime.utcnow().replace(tzinfo=pytz.utc).timestamp()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, str(now)))
    response = TextGenerationResponse(status=ResponseStatusEnum.PENDING, updated_at=now)
    redis.set(task_id, dict(response))
    celery.send_task(
        name="generate",
        kwargs={
            "task_id": task_id,
            "data": dict(data),
        },
        queue="llm",
    )
    return AsyncTaskResponse(task_id=task_id)


@router.get("/result/{task_id}")
async def get_result(request: Request, task_id: str) -> TextGenerationResponse:
    redis: Redis = request.app.state.redis
    data: Dict = redis.get(task_id)
    if data is None:
        raise HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail=f"Task ID({task_id}) not found")
    return TextGenerationResponse(status=data["status"], result=data["result"], updated_at=data["updated_at"])
