# Architecture

## Local development

```text
React/Vite frontend on localhost:5173
        |
        | HTTP
        v
FastAPI backend on localhost:8000
        |
        | boto3 / AWS SDK
        v
Amazon Bedrock Runtime
```

## AWS deployment

Recommended first deployment:

```text
User browser
        |
        v
Application Load Balancer
        |
        v
ECS Fargate service running FastAPI
        |
        v
Amazon Bedrock Runtime
```

Frontend options:

1. Serve frontend separately from S3 + CloudFront.
2. Serve built frontend assets from FastAPI.
3. Use Amplify for the frontend.

For the first simple project, option 1 or 2 is fine.

## Backend responsibilities

- Expose API endpoints.
- Enforce model allowlist.
- Validate request payloads.
- Convert app messages into Bedrock Converse API format.
- Normalize model responses.
- Handle AWS errors gracefully.
- Log request metadata without storing sensitive content by default.

## Bedrock responsibilities

- Provide access to foundation models.
- Handle model invocation.
- Integrate with AWS IAM, billing, CloudWatch, and regional controls.

## Security model

The ECS task receives an IAM role. That role can invoke only approved Bedrock model resources.

The browser receives no AWS credentials.
