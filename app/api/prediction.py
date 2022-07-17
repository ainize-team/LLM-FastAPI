from fastapi import APIRouter, Request
from payloads.request import TextGenerationRequest


router = APIRouter()


@router.post("/generate")
def post_generation(request: Request, data: TextGenerationRequest) -> str:
    tokenizer = request.app.state.tokenizer
    model = request.app.state.model
    input_ids = tokenizer(data.prompt, return_tensors="pt").input_ids.cuda()
    generated_ids = model.generate(input_ids)
    result = tokenizer.batch_decode(generated_ids, max_new_tokens=data.max_tokens, skip_special_tokens=True)
    return result[0]
