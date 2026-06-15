#!/usr/bin/env bash
set -euo pipefail

if [[ "${RUN_BEDROCK_SMOKE:-}" != "1" ]]; then
  printf 'Refusing to run Bedrock smoke test without RUN_BEDROCK_SMOKE=1.\n' >&2
  printf 'This test invokes AWS Bedrock and may incur usage charges.\n' >&2
  exit 2
fi

API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"
MODEL_KEY="${MODEL_KEY:-nova-lite}"
PROMPT="${PROMPT:-Reply with one short sentence confirming Bedrock is working.}"

response="$(
  curl -sS \
    -X POST \
    -H 'Content-Type: application/json' \
    -d "{\"model_key\":\"$MODEL_KEY\",\"message\":\"$PROMPT\",\"temperature\":0,\"max_tokens\":80}" \
    -w '\n%{http_code}' \
    "$API_BASE_URL/api/chat"
)"

status="$(printf '%s' "$response" | tail -n 1)"
payload="$(printf '%s' "$response" | sed '$d')"

if [[ "$status" != "200" ]]; then
  printf 'FAIL Bedrock chat: expected 200, got %s\n' "$status" >&2
  printf '%s\n' "$payload" >&2
  exit 1
fi

if printf '%s' "$payload" | grep -q 'Stub Bedrock response'; then
  printf 'FAIL Bedrock chat: backend is still returning the stub response.\n' >&2
  printf '%s\n' "$payload" >&2
  exit 1
fi

printf 'PASS Bedrock chat -> 200\n'
printf '%s\n' "$payload"
