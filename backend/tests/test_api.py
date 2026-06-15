from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "bedrock-model-router",
    }


def test_list_models_returns_allowlist():
    response = client.get("/api/models")

    assert response.status_code == 200
    body = response.json()
    assert body["models"] == [
        {
            "key": "nova-lite",
            "model_id": "amazon.nova-lite-v1:0",
            "label": "Amazon Nova Lite",
            "provider": "Amazon",
        },
        {
            "key": "claude-haiku",
            "model_id": "anthropic.claude-3-5-haiku-20241022-v1:0",
            "label": "Claude 3.5 Haiku",
            "provider": "Anthropic",
        },
    ]


def test_chat_returns_stub_response_for_allowed_model():
    response = client.post(
        "/api/chat",
        json={
            "model_key": "nova-lite",
            "message": "hello from pytest",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "model_key": "nova-lite",
        "model_id": "amazon.nova-lite-v1:0",
        "message": "Stub Bedrock response from amazon.nova-lite-v1:0: hello from pytest",
    }


def test_chat_rejects_unsupported_model_key():
    response = client.post(
        "/api/chat",
        json={
            "model_key": "not-allowed",
            "message": "hello",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported model_key"}


def test_chat_rejects_empty_message():
    response = client.post(
        "/api/chat",
        json={
            "model_key": "nova-lite",
            "message": "",
        },
    )

    assert response.status_code == 422
