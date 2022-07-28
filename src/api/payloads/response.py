from typing import List, Union

from pydantic import BaseModel

from ..enums import ResponseStatusEnum


class AsyncTaskResponse(BaseModel):
    task_id: str


class TextGenerationResponse(BaseModel):
    status: str = ResponseStatusEnum.PENDING.value
    result: Union[List[str], None] = None
