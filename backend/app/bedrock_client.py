"""Bedrock client wrapper.

Codex should implement this using boto3.client("bedrock-runtime") and the Converse API.
"""


class BedrockClient:
    def __init__(self, region_name: str):
        self.region_name = region_name

    def chat(self, model_id: str, user_text: str, temperature: float = 0.5, max_tokens: int = 1000) -> str:
        """Return assistant text.

        First implementation may return a stub.
        Later implementation should call Bedrock Runtime.
        """
        return f"Stub Bedrock response from {model_id}: {user_text}"
