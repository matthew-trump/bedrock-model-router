"""Application settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=REPO_ROOT / ".env")

    app_env: str = "local"
    aws_region: str = "us-west-2"
    bedrock_default_model: str = "amazon.nova-lite-v1:0"
    cors_origins: str = "http://localhost:5173"


settings = Settings()
