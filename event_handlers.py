import json
import os
from typing import Callable, Dict

import torch
from fastapi import FastAPI
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import model_settings


def _load_model(app: FastAPI) -> None:
    model_path = model_settings.model_path
    number_of_device = torch.cuda.device_count()
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
    app.state.tokenizer = AutoTokenizer.from_pretrained(model_path)
    app.state.model = AutoModelForCausalLM.from_pretrained(
        model_path, device_map=device_map, torch_dtype=torch.bfloat16
    )


def _shutdown_model(app: FastAPI) -> None:
    del app.state.model
    del app.state.tokenizer


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running App Start Handler.")
        _load_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running App Shutdown Handler.")
        _shutdown_model(app)

    return shutdown
