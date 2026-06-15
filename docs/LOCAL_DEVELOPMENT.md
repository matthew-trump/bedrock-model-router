# Local Development

This guide captures the first working local setup for Bedrock Model Router.

The current local app runs end to end with a stubbed Bedrock response:

```text
React/Vite frontend on 127.0.0.1:5173
        |
        | HTTP
        v
FastAPI backend on 127.0.0.1:8000
        |
        | stubbed BedrockClient.chat()
        v
fake model response
```

Real Bedrock invocation is the next milestone. AWS credentials can already be verified locally, but `backend/app/bedrock_client.py` still needs a `boto3` Converse implementation before prompts call Bedrock.

## Prerequisites

- Python 3.11 or newer
- Node.js and npm. Prefer Node.js 20, 22, or 24+ for the frontend test stack.
- AWS CLI v2, if testing real AWS access
- AWS credentials configured through the AWS CLI, SSO, environment variables, or another normal AWS credential provider

Do not store long-lived AWS access keys in `.env`. Use `aws configure sso`, `aws configure`, exported short-lived credentials, or IAM roles in deployed runtimes.

## Environment File

Create a local `.env` from the example:

```bash
cp .env.example .env
```

The local CORS setting should include both browser hostnames used during development:

```text
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

The backend loads the repo-root `.env` file from `backend/app/settings.py`, so it works when Uvicorn is launched from the `backend/` directory.

## Backend Setup

Create and activate a virtual environment:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
```

Install the backend package and dependencies:

```bash
python -m pip install -e ./backend
```

Install backend test dependencies:

```bash
python -m pip install -e './backend[test]'
```

Run the FastAPI app:

```bash
cd backend
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Frontend Setup

Install frontend dependencies:

```bash
cd frontend
npm install
```

Run the Vite dev server:

```bash
npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Open:

```text
http://127.0.0.1:5173
```

## Smoke Tests

From another terminal, verify the backend:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok","service":"bedrock-model-router"}
```

Verify the model registry:

```bash
curl http://127.0.0.1:8000/api/models
```

Verify stubbed chat:

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"model_key":"nova-lite","message":"hello from local test"}'
```

Expected behavior: the response includes the selected `model_key`, Bedrock `model_id`, and a message beginning with `Stub Bedrock response`.

Verify frontend build:

```bash
cd frontend
npm run build
```

Run frontend tests:

```bash
cd frontend
npm test
```

Install the Playwright browser binary once per machine:

```bash
cd frontend
npx playwright install chromium
```

Run browser/UI tests:

```bash
cd frontend
npm run test:e2e
```

The Playwright config reuses local servers on `127.0.0.1:8000` and `127.0.0.1:5173` when they are already running. If they are not running, it starts the FastAPI backend and Vite frontend for the test run.

Run backend tests:

```bash
cd backend
.venv/bin/python -m pytest
```

Run live local API smoke tests against a running backend:

```bash
scripts/smoke_api.sh
```

By default, the script targets `http://127.0.0.1:8000`. Override that with `API_BASE_URL` when needed:

```bash
API_BASE_URL=http://127.0.0.1:8001 scripts/smoke_api.sh
```

Run Docker Compose backend validation:

```bash
scripts/smoke_compose_backend.sh
```

This script builds and starts the Compose `backend` service, waits for `/health`, runs `scripts/smoke_api.sh`, and then stops the Compose stack. It defaults to host port `18000` to avoid collisions with other local services.

Override the host port if needed:

```bash
BACKEND_HOST_PORT=18001 scripts/smoke_compose_backend.sh
```

## AWS Credential Checks

Confirm the AWS CLI can see the active identity:

```bash
aws sts get-caller-identity
```

Confirm Bedrock is reachable in the configured region:

```bash
aws bedrock list-foundation-models \
  --region us-west-2 \
  --query 'modelSummaries[0:10].[modelId,providerName]' \
  --output table
```

These commands do not prove that a specific model can be invoked. Use the Layer 2 Bedrock smoke test below to validate a real model invocation through the local FastAPI app.

## Layer 2 Bedrock Smoke Test

Layer 2 uses the same local app, but switches the backend model client from `stub` to `bedrock`.

Run the Bedrock-mode backend smoke test with an explicit opt-in:

```bash
RUN_BEDROCK_SMOKE=1 scripts/smoke_bedrock_backend.sh
```

This starts a temporary backend on `http://127.0.0.1:18001` with:

```text
MODEL_CLIENT_MODE=bedrock
```

Then it calls `/api/chat` and fails if the response is still the stub response.

Validated result:

- `MODEL_KEY=nova-lite`
- `AWS_REGION=us-west-2`
- Bedrock model ID: `amazon.nova-lite-v1:0`
- Response returned through `/api/chat`: `Bedrock is working.`

This test requires:

- AWS credentials available to boto3
- Bedrock access in `AWS_REGION`
- access to the selected model
- awareness that the request may incur Bedrock usage charges

Override the model or prompt if needed:

```bash
RUN_BEDROCK_SMOKE=1 MODEL_KEY=claude-haiku PROMPT='Say hello.' scripts/smoke_bedrock_backend.sh
```

## Current Working State

- Backend dependencies install into `backend/.venv`.
- Frontend dependencies install with npm.
- `/health` returns healthy JSON.
- `/api/models` returns the local allowlist.
- `/api/chat` validates requests and routes to the configured model client.
- `MODEL_CLIENT_MODE=stub` keeps Layer 1 local testing deterministic and AWS-free.
- `MODEL_CLIENT_MODE=bedrock` enables real Bedrock Runtime `converse` calls.
- CORS allows the Vite frontend to call the backend locally.
- The frontend can select a model, submit a prompt, and display the stubbed response.
- AWS CLI credentials and Bedrock API reachability can be checked separately from the app.
- A real Layer 2 Bedrock smoke test has passed through the local app with `nova-lite`.

## Next Step

Improve AWS error handling around credential failures, model access issues, region mismatches, throttling, and malformed Bedrock responses.
