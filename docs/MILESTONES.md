# Milestones

## Milestone 1: Local backend skeleton

Deliver:

- [x] `GET /health`
- [x] `GET /api/models`
- [x] `POST /api/chat`
- [x] local stub response if Bedrock is not configured
- [x] Pydantic request and response models
- [x] local CORS for the Vite frontend

Success:

```bash
curl http://127.0.0.1:8000/health
```

returns healthy JSON.

Status: working locally with stubbed Bedrock responses.

## Milestone 2: Real Bedrock call

Deliver:

- `boto3` Bedrock Runtime client
- Converse API call
- model allowlist
- temperature/max token options

Success:

A local prompt returns a real model response from Bedrock.

## Milestone 3: Local frontend

Deliver:

- [x] simple chat UI
- [x] model selector
- [x] prompt input
- [x] response panel
- [x] loading and error states
- [x] TypeScript/Vite build config

Success:

User can chat with selected model from browser.

Status: working locally against the stubbed backend.

## Milestone 4: Docker

Deliver:

- backend Dockerfile
- docker-compose local run

Success:

Containerized backend works locally.

## Milestone 5: ECS deployment

Deliver:

- ECR repo
- ECS Fargate task
- ECS service
- ALB
- IAM task role
- CloudWatch logs

Success:

Public or private ALB endpoint returns `/health`, and `/api/chat` can invoke Bedrock.

## Milestone 6: Hardening

Deliver:

- CORS restriction
- model/resource-specific IAM
- basic rate limiting
- request size limits
- structured logging

## Milestone 7: Useful extensions

Possible extensions:

- streaming response endpoint
- saved conversations
- RAG
- prompt templates
- admin model configuration
- cost dashboard
