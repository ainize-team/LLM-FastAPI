from typing import List, Union

from pydantic import BaseModel

from enums import ResponseStatusEnum


class AsyncTaskResponse(BaseModel):
    task_id: str


class TextGenerationResponse(BaseModel):
    status: ResponseStatusEnum = ResponseStatusEnum.PENDING
    updated_at: float = 0.0
    result: Union[List[str], None] = None
