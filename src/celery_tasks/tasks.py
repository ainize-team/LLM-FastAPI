import json
import os
from typing import Dict, Union

import torch
from celery import Task
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

from utils import clear_memory

from .configs.config import model_settings
from .worker import app


class PredictTask(Task):
    def __init__(self):
        super().__init__()
        self.device = None
        self.tokenizer = None
        self.model = None

    def _load_model(self):
        model_path = model_settings.MODEL_PATH
        number_of_device = torch.cuda.device_count()
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=model_settings.USE_FAST_TOKENIZER)
        if number_of_device > 1:
            with open(os.path.join(model_path, "layer_list.json"), "r") as f:
                layer_list = json.load(f)
            n_layer = len(layer_list)
            quotient, remainder = divmod(n_layer, number_of_device)

            device_map: Dict[str, int] = {}
            idx = 0
            for i in range(number_of_device):
                for _ in range(quotient):
                    device_map[layer_list[idx]] = i
                    idx += 1
                if i >= number_of_device - remainder:
                    device_map[layer_list[idx]] = i
                    idx += 1

            logger.info(f"Device Map : {device_map}")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path, device_map=device_map, torch_dtype=torch.bfloat16
            ).cuda()
        else:
            logger.info("Load Model to Single GPU")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path, torch_dtype=torch.float16, low_cpu_mem_usage=True
            ).cuda()
        self.model.eval()

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            logger.info("Start loading model...")
            self._load_model()
            logger.info("Loading model is done!")

        return self.run(*args, **kwargs)


@app.task(name="generate", bind=True, base=PredictTask)
def generate(self, data: Dict) -> Union[str, Exception]:
    inputs = {
        "inputs": self.tokenizer.encode(data["prompt"], return_tensors="pt").cuda(),
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
        generated_ids = self.model.generate(**inputs)
    except ValueError as e:
        return {"status_code": 422, "message": e}
    except Exception as e:
        return {"status_code": 500, "message": e}
    finally:
        del inputs
    result = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    del generated_ids
    clear_memory()

    return result
