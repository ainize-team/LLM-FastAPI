from typing import List

from pydantic import BaseModel


class TextGenerationResponse(BaseModel):
    result: List[str]
