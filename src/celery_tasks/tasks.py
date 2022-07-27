from typing import Dict, List, Union

import torch
from celery.signals import celeryd_init
from loguru import logger

from .configs.config import model_settings
from .ml_model import LargeLanguageModel
from .utils import clear_memory
from .worker import app


llm = LargeLanguageModel()


@celeryd_init.connect
def load_model(**kwargs):
    logger.info("Start loading model...")
    llm.load_model(model_settings.model_path, model_settings.use_fast_tokenizer)
    logger.info("Loading model is done!")


@app.task(name="generate")
def generate(self, data: Dict) -> Union[List[str], Dict]:
    inputs = {
        "inputs": llm.tokenizer.encode(data["prompt"], return_tensors="pt").cuda()
        if torch.cuda.is_available()
        else llm.tokenizer.encode(data["prompt"], return_tensors="pt"),
        "max_new_tokens": data["max_new_tokens"],
        "do_sample": data["do_sample"],
        "early_stopping": data["early_stopping"],
        "num_beams": data["num_beams"],
        "temperature": data["temperature"],
        "top_k": data["top_k"],
        "top_p": data["top_p"],
        "no_repeat_ngram_size": data["no_repeat_ngram_size"],
        "num_return_sequences": data["num_return_sequences"],
    }

    try:
        generated_ids = llm.model.generate(**inputs)
    except ValueError as e:
        return {"status_code": 422, "message": str(e)}
    except Exception as e:
        return {"status_code": 500, "message": str(e)}
    finally:
        del inputs
    result = llm.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    del generated_ids
    clear_memory()

    return result
