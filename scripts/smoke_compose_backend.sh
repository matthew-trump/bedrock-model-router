#!/usr/bin/env bash
set -euo pipefail

BACKEND_HOST_PORT="${BACKEND_HOST_PORT:-18000}"
API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:$BACKEND_HOST_PORT}"
HEALTH_URL="$API_BASE_URL/health"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-30}"

cleanup() {
  docker compose down --remove-orphans
}

trap cleanup EXIT

BACKEND_HOST_PORT="$BACKEND_HOST_PORT" docker compose up -d --build backend

printf 'Waiting for backend health at %s\n' "$HEALTH_URL"

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  if curl -fsS "$HEALTH_URL" >/dev/null; then
    printf 'Backend is healthy after %s attempt(s).\n' "$attempt"
    API_BASE_URL="$API_BASE_URL" scripts/smoke_api.sh
    exit 0
  fi

  sleep 1
done

printf 'Backend did not become healthy after %s seconds.\n' "$MAX_ATTEMPTS" >&2
BACKEND_HOST_PORT="$BACKEND_HOST_PORT" docker compose logs backend >&2
exit 1
