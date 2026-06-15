# Project Brief

## Name

Bedrock Model Router

## Purpose

This is a small standalone project for learning how to build and deploy a web interface to Amazon Bedrock.

The application should let a user choose among a few allowed Bedrock models, type a prompt, and receive a model response.

## Core idea

The frontend is a normal browser app. The backend is the only component allowed to call AWS Bedrock.

```text
Browser
  -> Backend API
    -> AWS Bedrock Runtime
      -> selected foundation model
```

## Why this architecture

Calling Bedrock from the browser would expose credentials and would bypass server-side control. The backend provides:

- model allowlisting
- IAM isolation
- logging
- rate limiting later
- request validation
- cost controls
- prompt formatting
- future RAG integration

## Initial target

A single-user development app, not yet a multi-user SaaS product.

## Non-goals for the first version

- user accounts
- billing
- multi-tenant architecture
- production-grade auth
- streaming
- RAG
- saved chat history
- complex prompt management

Those can come later.
