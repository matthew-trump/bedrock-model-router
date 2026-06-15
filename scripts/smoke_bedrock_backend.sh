#!/usr/bin/env bash
set -euo pipefail

if [[ "${RUN_BEDROCK_SMOKE:-}" != "1" ]]; then
  printf 'Refusing to run Bedrock smoke test without RUN_BEDROCK_SMOKE=1.\n' >&2
  printf 'This test invokes AWS Bedrock and may incur usage charges.\n' >&2
  exit 2
fi

PORT="${BEDROCK_BACKEND_PORT:-18001}"
API_BASE_URL="http://127.0.0.1:$PORT"
LOG_FILE="${TMPDIR:-/tmp}/bedrock-model-router-bedrock-smoke.log"

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT

(
  cd backend
  MODEL_CLIENT_MODE=bedrock .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port "$PORT"
) >"$LOG_FILE" 2>&1 &

SERVER_PID="$!"

printf 'Waiting for Bedrock-mode backend at %s/health\n' "$API_BASE_URL"

for attempt in $(seq 1 30); do
  if curl -fsS "$API_BASE_URL/health" >/dev/null; then
    printf 'Backend is healthy after %s attempt(s).\n' "$attempt"
    API_BASE_URL="$API_BASE_URL" RUN_BEDROCK_SMOKE=1 scripts/smoke_bedrock_api.sh
    exit 0
  fi

  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    printf 'Backend process exited before becoming healthy.\n' >&2
    cat "$LOG_FILE" >&2
    exit 1
  fi

  sleep 1
done

printf 'Backend did not become healthy after 30 seconds.\n' >&2
cat "$LOG_FILE" >&2
exit 1
