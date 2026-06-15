# Bedrock Model Router

A small standalone learning project for building a private web app that routes chat requests to Amazon Bedrock models.

## Goal

Build a simple full-stack application:

```text
React/Vite frontend
        |
FastAPI backend
        |
AWS Bedrock Runtime
        |
Claude / Nova / Llama / Mistral / Cohere
```

The first working milestone is local development. The second milestone is deployment to AWS ECS Fargate.

## Suggested Codex starting command

Ask Codex:

> Read `.codex/START_HERE.md`, `docs/PROJECT_BRIEF.md`, and `docs/MILESTONES.md`. Then create the first working local backend milestone: FastAPI `/health`, `/api/models`, and a stubbed `/api/chat` endpoint. Do not deploy anything yet.

## Project layout

```text
bedrock-model-router/
  README.md
  .env.example
  docker-compose.yml

  .codex/
    START_HERE.md
    CODEX_TASKS.md

  docs/
    PROJECT_BRIEF.md
    ARCHITECTURE.md
    LOCAL_DEVELOPMENT.md
    MILESTONES.md
    AWS_DEPLOYMENT_NOTES.md
    BEDROCK_NOTES.md

  backend/
    Dockerfile
    pyproject.toml
    app/
      main.py
      settings.py
      models.py
      bedrock_client.py

  frontend/
    package.json
    index.html
    src/
      App.tsx
      api.ts
      components/
        ChatWindow.tsx
        ModelSelector.tsx

  infra/
    terraform/
      README.md
      main.tf
      variables.tf
      iam.tf
      ecr.tf
      ecs.tf
      alb.tf
```

## Initial development path

1. Implement backend locally.
2. Add Bedrock Runtime call using `boto3`.
3. Implement React chat UI.
4. Dockerize backend.
5. Deploy backend to ECS Fargate.
6. Optionally deploy frontend through S3 + CloudFront or serve it through the backend.
7. Add streaming, auth, logging, and RAG later.

## Local development

See `docs/LOCAL_DEVELOPMENT.md` for the repeatable setup path:

- create `.env`
- create the backend virtual environment
- install Python and npm dependencies
- run FastAPI and Vite locally
- smoke test `/health`, `/api/models`, `/api/chat`, CORS, and the frontend build
- verify AWS CLI and Bedrock API reachability

The current app runs locally with a stubbed Bedrock response. Real Bedrock invocation is the next milestone.
