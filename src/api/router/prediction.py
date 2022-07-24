from fastapi import APIRouter, Request

from celery_tasks.tasks import generate

from ..payloads.request import TextGenerationRequest
from ..payloads.response import AsyncTaskResponse


router = APIRouter()


@router.post("/generate")
def post_generation(request: Request, data: TextGenerationRequest) -> AsyncTaskResponse:
    task = generate.delay(dict(data))

    return AsyncTaskResponse(task_id=task.id)
