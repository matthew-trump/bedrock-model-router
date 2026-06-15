# Future Phase: Memory Layer Using DynamoDB and pgvector

## Status

Future phase.

Not part of the current implementation.

Codex should NOT implement this phase until explicitly instructed.

This document exists to guide future architectural work.

---

# Objective

Introduce persistent conversational memory into the application.

Goals:

* Store conversation history
* Retrieve relevant historical interactions
* Support long-running user relationships
* Support personalization
* Support memory-aware assistants

---

# High-Level Architecture

```text
User
  ↓

Application

  ↓

DynamoDB
  ↓
Embedding Worker
  ↓
PostgreSQL + pgvector

  ↓

Memory Retrieval Layer

  ↓

Prompt Builder

  ↓

LLM
```

---

# Design Philosophy

DynamoDB is the system of record.

PostgreSQL + pgvector is the semantic retrieval layer.

The vector store is NOT the primary memory store.

The vector store is a search index over memory.

---

# DynamoDB Responsibilities

## Purpose

Store durable conversational events.

Examples:

```text
User messages
Assistant messages
Conversation metadata
Session metadata
```

---

## Example Record

```json
{
  "user_id": "123",
  "conversation_id": "abc",
  "message_id": "xyz",
  "role": "user",
  "content": "Tell me about AWS Bedrock",
  "created_at": "2026-06-15T14:00:00Z"
}
```

---

## Why DynamoDB

Reasons:

* AWS-native
* Extremely scalable
* Low operational overhead
* Event-oriented data model
* Natural fit for chat history

---

# Local Development and Integration Tests

Use DynamoDB Local for development and integration tests.

DynamoDB access should be abstracted behind a repository or service layer.

Local tests should configure the DynamoDB client with:

```text
endpoint_url=http://localhost:18002
```

Deployed environments should omit `endpoint_url` and use real AWS DynamoDB resources provisioned by Terraform.

This keeps application code independent from whether the backing store is DynamoDB Local or AWS DynamoDB.

---

# PostgreSQL + pgvector Responsibilities

## Purpose

Semantic retrieval.

Examples:

* Relevant prior discussions
* Project decisions
* User preferences
* Historical summaries

---

## Example Table

```sql
CREATE TABLE memory_embeddings (
    id UUID PRIMARY KEY,
    user_id TEXT,
    conversation_id TEXT,
    message_id TEXT,
    summary TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMP
);
```

---

# Embedding Pipeline

Future asynchronous process:

```text
New Message
      ↓
Stored in DynamoDB
      ↓
Embedding Job
      ↓
Embedding Generated
      ↓
Stored in pgvector
```

Possible implementation:

* Lambda
* ECS Worker
* Celery Worker

Decision deferred.

---

# Retrieval Flow

## User Query

```text
How did we discuss Bedrock routing previously?
```

---

## Retrieval Process

1. Generate embedding for current query
2. Search pgvector
3. Retrieve top-N matches
4. Retrieve full records if necessary
5. Construct memory context
6. Invoke LLM

---

# Prompt Construction

Prompt builder may include:

```text
System Instructions

Relevant User Facts

Relevant Historical Memories

Current Conversation

Current Request
```

Only selected memories should be included.

Never include full historical conversations by default.

---

# Memory Categories

Future implementation should distinguish:

## Semantic Memory

Examples:

```text
User prefers Python
User uses AWS
User prefers Bedrock
```

---

## Episodic Memory

Examples:

```text
User discussed model routing
User selected DynamoDB
User rejected OpenSearch approach
```

Both memory types may ultimately be embedded and retrieved.

---

# Terraform Considerations

This phase should eventually be fully provisioned using Terraform.

Potential resources:

```text
DynamoDB Tables

RDS PostgreSQL

Security Groups

Parameter Store

Secrets Manager

IAM Roles

CloudWatch Logging
```

---

# Terraform Deferred

Terraform implementation is explicitly deferred.

Current phase should avoid:

* DynamoDB provisioning
* PostgreSQL provisioning
* RDS provisioning
* Memory retrieval implementation
* Embedding worker implementation

This phase is architectural planning only.

---

# Expected Future Deliverables

When this phase begins:

1. Terraform infrastructure
2. DynamoDB schema
3. PostgreSQL schema
4. pgvector setup
5. Embedding pipeline
6. Memory retrieval service
7. Prompt builder integration
8. End-to-end testing

---

# Success Criteria

The system should be capable of:

* Remembering prior conversations
* Retrieving relevant historical information
* Personalizing responses
* Maintaining bounded prompt sizes
* Scaling independently of model context window limitations

The memory subsystem should enhance the LLM rather than attempting to place all historical information directly into the context window.
