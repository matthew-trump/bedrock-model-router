# Bedrock Notes

## Mental model

Amazon Bedrock is AWS's managed platform for invoking foundation models.

Some models are Amazon's own models. Others are from providers such as Anthropic, Meta, Mistral, Cohere, and others.

The application talks to Bedrock through AWS APIs. It does not talk directly to third-party model-provider APIs.

## Recommended API

Use the Bedrock Runtime `converse` API for chat-style interactions where possible.

## Basic backend flow

```text
receive chat request
validate model key
look up Bedrock model ID
convert messages to Bedrock format
call bedrock-runtime converse
extract assistant text
return normalized response
```

## Model allowlist

Keep a local allowlist instead of accepting arbitrary model IDs from the frontend.

Example conceptual registry:

```python
ALLOWED_MODELS = {
    "nova-lite": {
        "model_id": "amazon.nova-lite-v1:0",
        "label": "Amazon Nova Lite",
    },
    "claude-haiku": {
        "model_id": "anthropic.claude-3-5-haiku-20241022-v1:0",
        "label": "Claude 3.5 Haiku",
    },
}
```

Model IDs should be verified against the current Bedrock console/docs for the region being used.

## Error cases to handle

- AWS credentials missing locally
- model access not enabled
- region mismatch
- throttling
- validation errors
- malformed messages
- model-specific unsupported parameters
