from typing import List, Union

from pydantic import BaseModel

from enums import ResponseStatusEnum


class TextGenerationResponse(BaseModel):
    status: str = ResponseStatusEnum.PENDING
    updated_at: float = 0.0
    result: Union[str, List[str], None] = None
