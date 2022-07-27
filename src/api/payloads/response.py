from typing import List

from pydantic import BaseModel, Field


class AsyncTaskResponse(BaseModel):
    task_id: str


class TextGenerationResponse(BaseModel):
    status: str = Field(
        default="wait",
        description="Check the result is generated. wait means the result is not ready yet.",
    )
    result: List[str] = Field(
        default=[""],
        description="If status is ok, it has the result value. Otherwise, default value.",
    )
