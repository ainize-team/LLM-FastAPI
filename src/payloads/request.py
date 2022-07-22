from pydantic import BaseModel, Field

from configs.config import model_settings


class TextGenerationRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_tokens=model_settings.MODEL_MAX_LENGTH << 2,
        description="The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.",
    )
    max_new_tokens: int = Field(
        default=16,
        gt=0,
        le=model_settings.MODEL_MAX_LENGTH,
        description="he maximum numbers of tokens to generate, ignore the current number of tokens.",
    )
    do_sample: bool = Field(
        default=True, description="Whether or not to use sampling ; use greedy decoding otherwise."
    )
    early_stopping: bool = Field(
        default=False,
        description="Whether to stop the beam search when at least num_beams sentences are finished per batch or not.",
    )
    num_beams: int = Field(default=1, description="Number of beams for beam search. 1 means no beam search.")
    temperature: float = Field(
        default=1.0,
        gt=0.0,
        description="he value used to module the next token probabilities.",
    )
    top_k: int = Field(
        default=50,
        gt=0,
        description="The number of highest probability vocabulary tokens to keep for top-k-filtering.",
    )
    top_p: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="If set to float < 1, only the most probable tokens with probabilities that add up to top_p or higher are kept for generation.",
    )
    no_repeat_ngram_size: int = Field(
        default=0, description="If set to int > 0, all ngrams of that size can only occur once."
    )
    num_return_sequences: int = Field(
        default=1,
        ge=1,
        le=5,
        description="The number of independently computed returned sequences for each element in the batch.",
    )
