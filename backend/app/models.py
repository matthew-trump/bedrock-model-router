"""Request/response models and model registry.

Codex should expand this file with Pydantic models.
"""

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
