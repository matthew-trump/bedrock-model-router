# AWS Local Testing Strategy: Three-Layer Development Model

## Purpose

This document describes the recommended development and testing strategy for AWS-targeted applications.

The goal is to maximize development velocity on a local machine (MacBook, workstation, etc.) while preserving a clean migration path to a fully deployed AWS environment.

The guiding principle is:

> We should be able to develop, test, debug, and validate the majority of application behavior locally without requiring AWS deployment.

At the same time, the architecture should anticipate eventual deployment into AWS using Terraform-provisioned infrastructure.

---

# Overview

The project uses a three-layer testing model.

```text
Layer 1
Local Development

        ↓

Layer 2
Local Integration With Select AWS Services

        ↓

Layer 3
AWS-Deployed Development Environment
```

Each layer provides increasing realism and increasing operational cost.

---

# Layer 1: Pure Local Development

## Purpose

Fastest development loop.

No AWS resources required.

Ideal for:

* Feature development
* Unit testing
* Integration testing
* Dataflow validation
* Local debugging

---

## Typical Components

```text
FastAPI
Worker Services
PostgreSQL
pgvector
Redis
DynamoDB Local
Mock Services
```

Typically executed using:

```bash
docker compose up
```

---

## Example Architecture

```text
Browser

   ↓

FastAPI

   ↓

PostgreSQL

   ↓

pgvector

   ↓

DynamoDB Local

   ↓

Worker Processes
```

---

## Benefits

* Extremely fast iteration
* No AWS costs
* Fully reproducible
* Easy onboarding
* Suitable for CI pipelines

---

## Limitations

Does not validate:

* IAM permissions
* AWS networking
* Security groups
* VPC routing
* CloudWatch integration
* Terraform deployments

---

# Layer 2: Local Integration With Select AWS Services

## Purpose

Validate interactions with selected AWS services while keeping most of the application local.

This layer is expected to be the primary development mode for many projects.

---

## Typical Components

Local:

```text
FastAPI
Workers
PostgreSQL
pgvector
DynamoDB Local
Redis
```

AWS:

```text
S3 Test Buckets
Bedrock
Selected APIs
```

---

## Example Architecture

```text
MacBook

FastAPI
Postgres
pgvector
DynamoDB Local

        ↓

AWS

S3 Test Bucket
Bedrock
```

---

## Why Use Real AWS Services Here?

Some services are inexpensive and difficult to simulate accurately.

Examples:

### S3

Benefits:

* Real object storage behavior
* Real permissions
* Real bucket structure

Cost:

Typically negligible.

### Bedrock

Benefits:

* Real model behavior
* Real token accounting
* Real latency measurements

Cost:

Usage-based.

---

## Recommended Usage

Dedicated development resources:

```text
myproject-dev-artifacts

myproject-test-documents

myproject-dev-scratch
```

Never share development buckets with production.

---

# Layer 3: AWS-Deployed Development Environment

## Purpose

Validate infrastructure and deployment behavior.

This layer is intentionally deferred during early development.

We acknowledge its future importance while avoiding premature complexity.

---

## Typical Components

Provisioned via Terraform:

```text
VPC

ECS

Lambda

RDS

DynamoDB

OpenSearch

S3

CloudWatch

IAM
```

---

## Example Architecture

```text
Terraform

      ↓

AWS Development Environment

      ↓

Application Deployment

      ↓

End-to-End Validation
```

---

## What Layer 3 Validates

* IAM policies
* Security groups
* VPC networking
* Deployment pipelines
* ECS behavior
* Lambda behavior
* CloudWatch logging
* Infrastructure scaling
* Terraform correctness

---

## What Layer 3 Is NOT

Layer 3 is not the primary development environment.

Developers should not need to deploy to AWS for routine feature development.

---

# Recommended Project Philosophy

For the foreseeable future:

Primary development should occur in:

```text
Layer 1
```

and

```text
Layer 2
```

Only occasional validation should require:

```text
Layer 3
```

---

# Example Future Memory Architecture

This aligns naturally with the planned memory subsystem.

## Local

```text
FastAPI

DynamoDB Local

PostgreSQL + pgvector

Embedding Worker
```

## AWS Integration

```text
Bedrock

S3 Test Bucket
```

## Future AWS Deployment

```text
DynamoDB

RDS PostgreSQL

pgvector

Terraform Provisioned Infrastructure
```

---

# Service Abstraction Requirement

Application code should never directly depend on deployment environment.

Use service interfaces:

```text
StorageService

MemoryRepository

EmbeddingService

ModelClient

MessageQueue
```

Environment configuration determines implementation.

Example:

## Local

```text
StorageService
  → Local Filesystem

MemoryRepository
  → DynamoDB Local
```

## AWS

```text
StorageService
  → S3

MemoryRepository
  → DynamoDB
```

Application logic remains unchanged.

---

# End-to-End Dataflow Testing

A successful local integration test should validate:

```text
User Request

      ↓

API Receives Request

      ↓

Message Stored

      ↓

Embedding Generated

      ↓

Vector Index Updated

      ↓

Memory Retrieved

      ↓

Prompt Constructed

      ↓

Model Invoked

      ↓

Response Stored

      ↓

Response Returned
```

The objective is not to recreate AWS perfectly.

The objective is to validate:

* application behavior
* data flow
* component interaction
* architectural integrity

before deployment.

---

# Long-Term Goal

Maintain a development workflow in which:

* most coding occurs locally
* integration testing occurs locally
* AWS costs remain minimal
* deployment remains predictable
* Terraform-managed infrastructure can be introduced later without major refactoring

This approach maximizes development speed while preserving a clean path toward production deployment.
