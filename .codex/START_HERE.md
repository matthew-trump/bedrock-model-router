# Codex Start Here

You are helping build `bedrock-model-router`, a standalone AWS Bedrock learning project.

## First objective

Create a minimal local app before attempting AWS deployment.

Start with the backend:

- FastAPI app
- `GET /health`
- `GET /api/models`
- `POST /api/chat`
- model registry
- Bedrock client wrapper
- graceful fallback/stub mode if AWS credentials or model access are unavailable

Do not create production auth yet. Do not deploy yet.

## Important constraints

- Keep the project simple.
- Prefer readable code over clever abstractions.
- Do not hard-code secrets.
- Browser must never call Bedrock directly.
- All Bedrock calls must go through the backend.
- Maintain an explicit allowlist of model IDs.
- Make each milestone runnable.

## After backend milestone

Then build:

- React/Vite frontend
- local chat UI
- model selector
- request/response rendering

Then:

- Docker image
- ECR
- ECS Fargate
- ALB
- IAM task role for Bedrock invocation
- CloudWatch logs

## Recommended working style

Make small commits or checkpoint summaries after each milestone.
Update docs when implementation decisions change.
