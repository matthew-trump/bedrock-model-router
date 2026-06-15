# LLM Memory Architecture Notes

## Purpose

This document summarizes architectural discussions regarding memory management in LLM-powered applications, with particular focus on:

* Context windows
* Episodic memory
* Semantic memory
* Relational databases
* NoSQL databases
* Vector databases and vector indexes
* AWS-oriented implementation patterns

The goal is to understand how production systems maintain information across multiple LLM requests despite the fact that LLMs themselves possess no persistent conversational memory.

---

# Core Principle

An LLM does not retain conversational state between API requests.

Each request is effectively independent.

Any information that should influence the current response must be included in the prompt for the current inference.

Examples:

* User identity
* User preferences
* Conversation history
* Retrieved documents
* Prior decisions
* Organizational knowledge

must all be reintroduced into the model's context window when needed.

---

# Context Window

The context window represents the model's working memory for a single inference.

Typical prompt contents:

```text
System Instructions
+
User Information
+
Conversation History
+
Retrieved Documents
+
Current User Request
```

The model only sees what is included in this context.

After the inference completes, the context disappears.

---

# Three Types of Memory

## Working Memory

Short-term memory.

Exists only inside the context window.

Examples:

* Current question
* Current retrieved documents
* Recent conversation turns

Lifetime:

* One inference

---

## Episodic Memory

Historical interactions.

Examples:

* Previous conversations
* Decisions made by the user
* Historical events in a project

Examples:

```text
User discussed AWS Bedrock on June 15.

User decided to use DynamoDB for message storage.

User selected Claude Sonnet for testing.
```

Lifetime:

* Months or years

---

## Semantic Memory

Persistent facts.

Examples:

```text
User name is Matthew.

User prefers Python.

User uses AWS.

User is building AI applications.
```

Lifetime:

* Months or years

Semantic memory changes slowly.

---

# Why Databases Are Required

The LLM is not a database.

The application is responsible for:

1. Storing information
2. Retrieving information
3. Selecting relevant information
4. Injecting information into prompts

A typical architecture is:

```text
Databases
     ↓
Memory Retrieval
     ↓
Prompt Builder
     ↓
LLM
```

---

# Relational Databases

Examples:

* PostgreSQL
* MySQL

Strengths:

* Strong consistency
* SQL querying
* Complex relationships
* Excellent tooling
* Mature ecosystem

Typical usage:

```text
User Profiles
Projects
Tasks
Structured Memory
Metadata
```

Relational databases are usually the simplest solution for semantic memory.

---

# NoSQL Databases

Examples:

* DynamoDB
* MongoDB

Strengths:

* Horizontal scaling
* Flexible schemas
* High write throughput
* AWS-native integration

Typical usage:

```text
Conversation Events
Chat Messages
Sessions
User Activity
Request Logs
```

DynamoDB is particularly attractive for large-scale conversation storage because conversations naturally resemble event streams.

---

# Vector Databases and Vector Indexes

Examples:

* pgvector
* OpenSearch Vector Search
* Pinecone
* Weaviate
* Qdrant
* Chroma

Purpose:

Semantic retrieval.

Instead of asking:

```text
Find messages from June 1.
```

we ask:

```text
Find messages similar to:
"Bedrock model routing discussion"
```

Embeddings enable meaning-based retrieval.

---

# Important Distinction

A vector store is usually NOT the source of truth.

Instead:

```text
Source of Truth
     ↓
Embeddings
     ↓
Vector Index
```

The vector index is primarily a search layer.

---

# Common Production Pattern

## Step 1

Store raw conversation history.

Example:

```text
DynamoDB
```

Stores:

* User messages
* Assistant messages
* Metadata
* Timestamps

---

## Step 2

Generate embeddings.

Examples:

```text
Message
Conversation Summary
Decision Record
Task Summary
```

---

## Step 3

Store embeddings.

Examples:

```text
pgvector
OpenSearch
Pinecone
```

---

## Step 4

At inference time

1. User sends query
2. Query embedding generated
3. Semantic search performed
4. Relevant memories retrieved
5. Prompt assembled
6. LLM invoked

---

# Why Not Put Everything Into Context?

Problems:

* Increased cost
* Increased latency
* Context limits
* Reduced relevance

Most production systems retrieve only the most relevant memories.

This is the same principle used in Retrieval Augmented Generation (RAG).

---

# Architectural Conclusion

Recommended conceptual model:

```text
LLM
  =
CPU

Context Window
  =
RAM

Databases
  =
Disk Storage
```

The databases hold long-term memory.

The vector index helps decide what information should be loaded into working memory.

The context window contains only the information required for the current inference.
