# Layer 2 Local AWS Integration Testing: To Do

## Goal

Validate the local application against selected real AWS services while preserving all Layer 1 local/stub testing.

Layer 2 is opt-in. It should never replace or weaken Layer 1.

## Completed

- Model client mode added through configuration:
  - `MODEL_CLIENT_MODE=stub`
  - `MODEL_CLIENT_MODE=bedrock`
- Stub model client remains the default.
- Bedrock model client added using `boto3.client("bedrock-runtime").converse(...)`.
- Layer 1 tests continue to run without AWS credentials or Bedrock access.
- Bedrock smoke scripts added:
  - `scripts/smoke_bedrock_api.sh`
  - `scripts/smoke_bedrock_backend.sh`
- Real Bedrock smoke passed with `MODEL_KEY=nova-lite` in `us-west-2`.

## Remaining

- Add more graceful AWS error mapping if the first real calls expose useful cases.
