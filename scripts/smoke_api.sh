#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"

request() {
  local method="$1"
  local path="$2"
  local expected_status="$3"
  local body="${4:-}"

  local response
  if [[ -n "$body" ]]; then
    response="$(
      curl -sS \
        -X "$method" \
        -H 'Content-Type: application/json' \
        -d "$body" \
        -w '\n%{http_code}' \
        "$API_BASE_URL$path"
    )"
  else
    response="$(curl -sS -X "$method" -w '\n%{http_code}' "$API_BASE_URL$path")"
  fi

  local status
  status="$(printf '%s' "$response" | tail -n 1)"

  local payload
  payload="$(printf '%s' "$response" | sed '$d')"

  if [[ "$status" != "$expected_status" ]]; then
    printf 'FAIL %s %s: expected %s, got %s\n' "$method" "$path" "$expected_status" "$status" >&2
    printf '%s\n' "$payload" >&2
    exit 1
  fi

  printf 'PASS %s %s -> %s\n' "$method" "$path" "$status"
  printf '%s\n' "$payload"
}

request GET /health 200
request GET /api/models 200
request POST /api/chat 200 '{"model_key":"nova-lite","message":"hello from smoke test"}'
request POST /api/chat 400 '{"model_key":"not-allowed","message":"hello"}'
request POST /api/chat 422 '{"model_key":"nova-lite","message":""}'
