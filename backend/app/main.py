"""FastAPI entry point.

Codex should implement this file first.
"""

from fastapi import FastAPI

app = FastAPI(title="Bedrock Model Router")


@app.get("/health")
def health():
    return {"status": "ok", "service": "bedrock-model-router"}


@app.get("/api/models")
def list_models():
    # TODO: return allowed model registry from models.py
    return {"models": []}


@app.post("/api/chat")
def chat():
    # TODO: validate request, call BedrockClient, return normalized response
    return {
        "message": "Stub response. Implement Bedrock integration in backend/app/bedrock_client.py."
    }
