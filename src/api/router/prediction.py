from typing import Dict

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, Request

from celery_tasks.tasks import generate

from ..payloads.request import TextGenerationRequest
from ..payloads.response import AsyncTaskResponse, TextGenerationResponse


router = APIRouter()


@router.post("/generate")
def post_generation(request: Request, data: TextGenerationRequest) -> AsyncTaskResponse:
    task = generate.delay(dict(data))
    return AsyncTaskResponse(task_id=task.id)


@router.get("/result/{task_id}")
def get_result(request: Request, task_id: str) -> TextGenerationResponse:
    task = AsyncResult(task_id)
    if not task.ready():
        return TextGenerationResponse()
    result = task.get()
    if type(result) == Dict:
        raise HTTPException(result["status_code"], result["message"])
    return TextGenerationResponse(status="ok", result=result)
