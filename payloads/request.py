from pydantic import BaseModel, Field


class TextGenerationRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_tokens=8192,
        description="The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.",
    )
    max_tokens: int = Field(
        default=16,
        gt=0,
        le=2048,
        description="The maximum number of tokens to generate in the completion. The token count of your prompt plus max_tokens cannot exceed the model's context length.",
    )
    temperature: float = Field(
        default=0.9,
        gt=0.0,
        description="What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer. We generally recommend altering this or `top_p` but not both.",
    )
    top_k: int = Field(
        default=50, description="The number of highest probability vocabulary tokens to keep for top-k-filtering."
    )
    top_p: float = Field(
        default=0.95,
        ge=0.0,
        le=1.0,
        description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.",
    )
    repetition_penalty: float = Field(
        default=0.8, gt=0.0, description="The parameter for repetition penalty. 1.0 means no penalty."
    )
    do_sample: bool = Field(
        default=True, description="Whether or not to use sampling ; use greedy decoding otherwise."
    )
