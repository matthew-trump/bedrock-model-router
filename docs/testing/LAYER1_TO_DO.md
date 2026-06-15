# Layer 1 Local Testing: To Do

## Completed

- Backend test framework installed: `pytest`.
- Backend API tests added for `/health`, `/api/models`, and `/api/chat`.
- Backend validation tests added for unsupported model keys and empty messages.
- Live local API smoke script added: `scripts/smoke_api.sh`.
- Local API smoke testing verifies expected `200`, `400`, and `422` responses against a running FastAPI server.
- Frontend test framework installed: `vitest`.
- Frontend component tests added with React Testing Library.
- Frontend tests cover model loading, prompt submission, loading state, error state, blank-prompt disabled state, and response rendering.
- Browser/UI test framework installed: Playwright.
- Playwright e2e test added for loading models and submitting a prompt through the local backend.
- Docker Compose backend smoke script added: `scripts/smoke_compose_backend.sh`.
- Docker Compose validation defaults to host port `18000` to avoid collisions with other local services on port `8000`.
- Docker Compose validation passed for the containerized backend.
- Local testing instructions documented in `docs/LOCAL_DEVELOPMENT.md`.

## Live API Smoke Script

Run the live local API smoke test with:

```bash
scripts/smoke_api.sh
```

The script defaults to `http://127.0.0.1:18000`. Override the target backend with:

```bash
API_BASE_URL=http://127.0.0.1:18001 scripts/smoke_api.sh
```

## Remaining

- No remaining Layer 1 local testing items at this time.

## Deferred

- DynamoDB Local, PostgreSQL, and pgvector tests are deferred until the future memory phase begins.
