# Codex Task List

## Milestone 1 — Local backend

- [ ] Create FastAPI app.
- [ ] Add `/health`.
- [ ] Add `/api/models`.
- [ ] Add `/api/chat`.
- [ ] Add Pydantic request/response models.
- [ ] Add model allowlist.
- [ ] Add `BedrockClient` wrapper.
- [ ] Add stub mode for local testing without AWS access.
- [ ] Add basic error handling.

## Milestone 2 — Bedrock integration

- [ ] Use `boto3.client("bedrock-runtime")`.
- [ ] Implement `converse` call.
- [ ] Normalize response text.
- [ ] Add max token and temperature parameters.
- [ ] Add AWS region setting.
- [ ] Verify model access in AWS console.

## Milestone 3 — Frontend

- [ ] Create Vite React app.
- [ ] Build chat input.
- [ ] Build message display.
- [ ] Build model selector.
- [ ] Connect to backend.
- [ ] Add loading/error states.

## Milestone 4 — Containerization

- [ ] Backend Dockerfile.
- [ ] Local docker-compose.
- [ ] Confirm `/health` in container.
- [ ] Confirm `/api/chat` in container.

## Milestone 5 — AWS deployment

- [ ] ECR repository.
- [ ] ECS cluster.
- [ ] ECS Fargate task definition.
- [ ] ECS service.
- [ ] ALB.
- [ ] IAM task role with Bedrock invoke permissions.
- [ ] CloudWatch logs.
- [ ] Deployment docs.

## Later milestones

- [ ] Streaming responses.
- [ ] User auth.
- [ ] Request logging.
- [ ] Cost controls.
- [ ] RAG using Bedrock Knowledge Bases or custom vector store.
- [ ] Prompt templates.
