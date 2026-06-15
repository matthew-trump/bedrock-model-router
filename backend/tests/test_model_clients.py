import pytest

from app.bedrock_client import ModelClientError, StubModelClient, _extract_text


def test_stub_model_client_returns_deterministic_response():
    client = StubModelClient()

    response = client.chat(
        model_id="test-model",
        user_text="hello",
        temperature=0.1,
        max_tokens=10,
    )

    assert response == "Stub Bedrock response from test-model: hello"


def test_extract_text_returns_concatenated_bedrock_text_blocks():
    response = {
        "output": {
            "message": {
                "content": [
                    {"text": "hello"},
                    {"text": " world"},
                ]
            }
        }
    }

    assert _extract_text(response) == "hello world"


def test_extract_text_rejects_response_without_text():
    with pytest.raises(ModelClientError, match="assistant text"):
        _extract_text({"output": {"message": {"content": []}}})
