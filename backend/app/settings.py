"""Application settings."""

from pathlib import Path

from pydantic_settings import BaseSettings

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_env: str = "local"
    aws_region: str = "us-west-2"
    bedrock_default_model: str = "amazon.nova-lite-v1:0"
    cors_origins: str = "http://localhost:5173"

    class Config:
        env_file = REPO_ROOT / ".env"


settings = Settings()
