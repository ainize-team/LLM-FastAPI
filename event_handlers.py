from typing import Callable, Dict, List

import torch
from fastapi import FastAPI
from loguru import logger
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

from config import model_settings


def _load_model(app: FastAPI) -> None:
    model_name_or_path = model_settings.model_name_or_path
    number_of_device = torch.cuda.device_count()
    config = AutoConfig.from_pretrained(model_name_or_path)
    n_layer = config.n_layer
    quotient, remainder = divmod(n_layer, number_of_device)
    device_map: Dict[int, List[int]] = {}
    for device_number in range(number_of_device - 1, -1, -1):
        device_map[device_number] = []
        for _ in range(quotient):
            n_layer -= 1
            device_map[device_number].append(n_layer)
        if remainder:
            remainder -= 1
            n_layer -= 1
            device_map[device_number].append(n_layer)
    logger.info(f"Device Map : {device_map}")
    app.state.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    app.state.model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path, device_map=device_map, torch_dtype=torch.bfloat16
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
