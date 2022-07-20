from fastapi import APIRouter, HTTPException, Request

from payloads.request import TextGenerationRequest
from payloads.response import TextGenerationResponse
from utils import clear_memory


router = APIRouter()


@router.post("/generate")
def post_generation(request: Request, data: TextGenerationRequest) -> TextGenerationResponse:
    tokenizer = request.app.state.tokenizer
    model = request.app.state.model
    inputs = {
        "inputs": tokenizer(data.prompt, return_tensors="pt").input_ids.cuda(),
        "max_new_tokens": data.max_new_tokens,
        "do_sample": data.do_sample,
        "early_stopping": data.early_stopping,
        "num_beams": data.num_beams,
        "temperature": data.temperature,
        "top_k": data.top_k,
        "top_p": data.top_p,
        "no_repeat_ngram_size": data.no_repeat_ngram_size,
        "num_return_sequences": data.num_return_sequences,
    }
    try:
        generated_ids = model.generate(**inputs)
    except ValueError as e:
        raise HTTPException(422, e)
    except Exception as e:
        raise HTTPException(500, e)
    finally:
        del inputs
    result = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    del generated_ids
    clear_memory()
    return TextGenerationResponse(result=result)
