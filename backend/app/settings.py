"""Application settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "local"
    aws_region: str = "us-west-2"
    bedrock_default_model: str = "amazon.nova-lite-v1:0"
    cors_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()
