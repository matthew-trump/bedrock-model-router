"""Model client wrappers."""

from typing import Protocol


import boto3
from botocore.exceptions import BotoCoreError, ClientError


class ModelClientError(RuntimeError):
    """Raised when a model provider call fails."""


class ModelClient(Protocol):
    def chat(
        self,
        model_id: str,
        user_text: str,
        temperature: float = 0.5,
        max_tokens: int = 1000,
    ) -> str:
        """Return assistant text."""


class StubModelClient:
    def chat(
        self,
        model_id: str,
        user_text: str,
        temperature: float = 0.5,
        max_tokens: int = 1000,
    ) -> str:
        return f"Stub Bedrock response from {model_id}: {user_text}"


class BedrockModelClient:
    def __init__(self, region_name: str):
        self.region_name = region_name
        self._client = boto3.client("bedrock-runtime", region_name=region_name)

    def chat(
        self,
        model_id: str,
        user_text: str,
        temperature: float = 0.5,
        max_tokens: int = 1000,
    ) -> str:
        try:
            response = self._client.converse(
                modelId=model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": user_text}],
                    }
                ],
                inferenceConfig={
                    "temperature": temperature,
                    "maxTokens": max_tokens,
                },
            )
        except (BotoCoreError, ClientError) as error:
            raise ModelClientError(str(error)) from error

        return _extract_text(response)


def create_model_client(mode: str, region_name: str) -> ModelClient:
    if mode == "stub":
        return StubModelClient()
    if mode == "bedrock":
        return BedrockModelClient(region_name=region_name)
    raise ValueError(f"Unsupported model client mode: {mode}")


def _extract_text(response: dict) -> str:
    content = (
        response.get("output", {})
        .get("message", {})
        .get("content", [])
    )
    text_parts = [
        block["text"]
        for block in content
        if isinstance(block, dict) and isinstance(block.get("text"), str)
    ]
    if not text_parts:
        raise ModelClientError("Bedrock response did not include assistant text")
    return "".join(text_parts)
