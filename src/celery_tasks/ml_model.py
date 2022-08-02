import json
import os
from typing import Dict

import torch
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer


class CausalLMHuggingfaceModel:
    def __init__(self):
        self.tokenizer = None
        self.model = None

    def load_model(self, model_path: str, use_fast: bool = True):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=use_fast)
        if torch.cuda.is_available():
            self.model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16).cuda()
        else:
            self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.model.eval()


class LargeLanguageModel(CausalLMHuggingfaceModel):
    def __init__(self):
        super(LargeLanguageModel, self).__init__()

    def load_model(self, model_path: str, use_fast: bool = True):
        number_of_device = torch.cuda.device_count()
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=use_fast)

        if torch.cuda.is_available():
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
                )
            else:
                logger.info("Load Model to Single GPU")
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path, torch_dtype=torch.float16, low_cpu_mem_usage=True
                ).cuda()
        else:
            self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.model.eval()
