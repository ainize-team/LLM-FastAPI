from typing import Callable, Dict

import torch
from fastapi import FastAPI
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import model_settings


def _load_model(app: FastAPI) -> None:
    model_name_or_path = model_settings.model_name_or_path
    # TODO: generalize
    number_of_device = torch.cuda.device_count()
    layer_list = [
        "transformer.word_embeddings",
        "lm_head",
        "transformer.word_embeddings_layernorm",
        "transformer.h.0",
        "transformer.h.1",
        "transformer.h.2",
        "transformer.h.3",
        "transformer.h.4",
        "transformer.h.5",
        "transformer.h.6",
        "transformer.h.7",
        "transformer.h.8",
        "transformer.h.9",
        "transformer.h.10",
        "transformer.h.11",
        "transformer.h.12",
        "transformer.h.13",
        "transformer.h.14",
        "transformer.h.15",
        "transformer.h.16",
        "transformer.h.17",
        "transformer.h.18",
        "transformer.h.19",
        "transformer.h.20",
        "transformer.h.21",
        "transformer.h.22",
        "transformer.h.23",
        "transformer.h.24",
        "transformer.h.25",
        "transformer.h.26",
        "transformer.h.27",
        "transformer.h.28",
        "transformer.h.29",
        "transformer.h.30",
        "transformer.h.31",
        "transformer.h.32",
        "transformer.h.33",
        "transformer.h.34",
        "transformer.h.35",
        "transformer.h.36",
        "transformer.h.37",
        "transformer.h.38",
        "transformer.h.39",
        "transformer.h.40",
        "transformer.h.41",
        "transformer.h.42",
        "transformer.h.43",
        "transformer.h.44",
        "transformer.h.45",
        "transformer.h.46",
        "transformer.h.47",
        "transformer.h.48",
        "transformer.h.49",
        "transformer.h.50",
        "transformer.h.51",
        "transformer.h.52",
        "transformer.h.53",
        "transformer.h.54",
        "transformer.h.55",
        "transformer.h.56",
        "transformer.h.57",
        "transformer.h.58",
        "transformer.h.59",
        "transformer.h.60",
        "transformer.h.61",
        "transformer.h.62",
        "transformer.h.63",
        "transformer.h.64",
        "transformer.h.65",
        "transformer.h.66",
        "transformer.h.67",
        "transformer.h.68",
        "transformer.h.69",
        "transformer.ln_f",
    ]
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
