from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, Request

from celery_tasks.tasks import generate

from ..enums import ResponseStatusEnum
from ..payloads.request import TextGenerationRequest
from ..payloads.response import AsyncTaskResponse, TextGenerationResponse


router = APIRouter()


@router.post("/generate")
def post_generation(request: Request, data: TextGenerationRequest) -> AsyncTaskResponse:
    task = generate.delay(dict(data))
    return AsyncTaskResponse(task_id=task.id)


@router.get("/result/{task_id}")
async def get_result(request: Request, task_id: str) -> TextGenerationResponse:
    task = AsyncResult(task_id)
    try:
        check = task.ready()
    except ValueError as e:
        raise HTTPException(422, e)
    except Exception as e:
        raise HTTPException(500, e)
    if not check:
        return TextGenerationResponse(status=ResponseStatusEnum.ASSIGNED)
    result = task.get()
    if isinstance(result, dict):
        raise HTTPException(result["status_code"], result["message"])
    return TextGenerationResponse(status=ResponseStatusEnum.COMPLETED, result=result)
