from fastapi import APIRouter, Request

from payloads.request import TextGenerationRequest
from utils import clear_memory


router = APIRouter()


@router.post("/generate")
def post_generation(request: Request, data: TextGenerationRequest) -> str:
    tokenizer = request.app.state.tokenizer
    model = request.app.state.model
    input_ids = tokenizer(data.prompt, return_tensors="pt").input_ids.cuda()
    generated_ids = model.generate(
        input_ids,
        max_new_tokens=data.max_tokens,
        temperature=data.temperature,
        top_k=data.top_k,
        top_p=data.top_p,
        repetition_penalty=data.repetition_penalty,
        do_sample=data.do_sample,
    )
    result = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    clear_memory()
    return result[0]
