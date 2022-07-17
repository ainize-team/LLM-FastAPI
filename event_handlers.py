from typing import Callable

import torch
from fastapi import FastAPI
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import model_settings


def _load_model(app: FastAPI) -> None:
    model_name_or_path = model_settings.model_name_or_path
    app.state.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    app.state.model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path, device_map="auto", torch_dtype=torch.float16
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
