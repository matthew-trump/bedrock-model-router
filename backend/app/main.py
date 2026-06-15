"""FastAPI entry point."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.bedrock_client import ModelClientError, create_model_client
from app.models import ALLOWED_MODELS, ChatRequest, ChatResponse, ModelInfo, ModelsResponse
from app.settings import settings

app = FastAPI(title="Bedrock Model Router")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_client = create_model_client(
    mode=settings.model_client_mode,
    region_name=settings.aws_region,
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "bedrock-model-router"}


@app.get("/api/models", response_model=ModelsResponse)
def list_models() -> ModelsResponse:
    return ModelsResponse(
        models=[
            ModelInfo(key=key, **model_config)
            for key, model_config in ALLOWED_MODELS.items()
        ]
    )


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    model_config = ALLOWED_MODELS.get(request.model_key)
    if model_config is None:
        raise HTTPException(status_code=400, detail="Unsupported model_key")

    try:
        message = model_client.chat(
            model_id=model_config["model_id"],
            user_text=request.message,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
    except ModelClientError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

    return ChatResponse(
        model_key=request.model_key,
        model_id=model_config["model_id"],
        message=message,
    )
