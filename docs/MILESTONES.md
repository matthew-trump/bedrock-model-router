# Milestones

## Milestone 1: Local backend skeleton

Deliver:

- `GET /health`
- `GET /api/models`
- `POST /api/chat`
- local stub response if Bedrock is not configured

Success:

```bash
curl http://localhost:8000/health
```

returns healthy JSON.

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

- simple chat UI
- model selector
- prompt input
- response panel

Success:

User can chat with selected model from browser.

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
