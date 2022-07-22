from pydantic import BaseModel


class AsyncTaskResponse(BaseModel):
    task_id: str
