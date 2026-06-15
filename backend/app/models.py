"""Request/response models and model registry."""

from pydantic import BaseModel, Field

ALLOWED_MODELS = {
    "nova-lite": {
        "model_id": "amazon.nova-lite-v1:0",
        "label": "Amazon Nova Lite",
        "provider": "Amazon",
    },
    "claude-haiku": {
        "model_id": "anthropic.claude-3-5-haiku-20241022-v1:0",
        "label": "Claude 3.5 Haiku",
        "provider": "Anthropic",
    },
}


class ModelInfo(BaseModel):
    key: str
    model_id: str
    label: str
    provider: str


class ModelsResponse(BaseModel):
    models: list[ModelInfo]


class ChatRequest(BaseModel):
    model_key: str = Field(default="nova-lite")
    message: str = Field(min_length=1, max_length=20_000)
    temperature: float = Field(default=0.5, ge=0, le=1)
    max_tokens: int = Field(default=1000, ge=1, le=4096)


class ChatResponse(BaseModel):
    model_key: str
    model_id: str
    message: str
