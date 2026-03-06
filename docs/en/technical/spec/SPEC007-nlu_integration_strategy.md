---
code: SPEC007
title: NLU Integration Strategy (Rasa)
status: Proposed
author: Elias M. P. Junior
date: 2026-03-06
tags: architecture, nlu, rasa, adapter
---

# SPEC007: NLU Integration Strategy (Rasa)

## 1. Context

The current OntoBDC interface is primarily CLI-based, requiring users to know exact commands and flags (e.g., `ontobdc list --type pdf`). To support **Natural Language Understanding (NLU)** and enable conversational interfaces (Chatbots, Voice Assistants), we need a strategy to translate human language into executable OntoBDC Capabilities.

The user has expressed a specific preference for using **Rasa** as the NLU engine.

## 2. The Challenge

*   **Complexity:** Rasa is a heavy framework that typically runs as a separate service (HTTP API). Embedding it directly into the `ontobdc` Python package would bloat dependencies and complicate distribution.
*   **Mapping:** There is a semantic gap between a user's intent (e.g., "Show me the contracts") and the technical Capability (e.g., `list_documents(pattern="*contract*")`).

## 3. Decision: Adapter Pattern with External Service

We will adopt an **Adapter-based architecture** where Rasa runs as an external service (e.g., a Docker container), and OntoBDC acts as the execution client.

### 3.1. Architecture Components

1.  **Rasa Server (The Brain)**:
    *   Responsible for **Intent Classification** and **Entity Extraction**.
    *   Example Input: "Encontre os PDFs do projeto"
    *   Example Output: `{"intent": "find_resources", "entities": {"resource_type": "pdf"}}`

2.  **NLU Adapter (The Translator)**:
    *   A component within `ontobdc-core` (`ontobdc.core.adapter.nlu`).
    *   Sends text to the Rasa API.
    *   Receives the structured Intent/Entities.
    *   **Crucial Step:** Maps the Rasa Intent to an OntoBDC Capability.

3.  **Capability Runtime (The Executor)**:
    *   Executes the resolved Capability with the extracted parameters.

### 3.2. Mapping Strategy (Intent -> Capability)

A configuration file (e.g., `nlu_map.yaml`) will define how intents map to capabilities.

```yaml
intents:
  find_resources:
    capability: resource.list_documents
    params:
      resource_type: type  # Maps entity 'resource_type' to arg 'type'
  
  extract_data:
    capability: drive.pdf.extract_text
    params:
      target_file: path
```

## 4. Implementation Stages

### Stage 1: The Sidecar (Docker)
Add a Rasa service to the `ontobdc-stack` Docker Compose. This keeps the environment isolated and clean.

```yaml
services:
  rasa:
    image: rasa/rasa:3.x
    volumes:
      - ./rasa-project:/app
    command: ["run", "--enable-api"]
```

### Stage 2: The CLI Command
Add a command `ontobdc chat "message"` that:
1.  POSTs the message to `http://localhost:5005/model/parse`.
2.  Resolves the capability via `nlu_map.yaml`.
3.  Executes the capability and returns the result.

## 5. Why this approach?

*   **Decoupling:** OntoBDC remains lightweight. You only need Rasa if you want NLU features.
*   **Scalability:** The Rasa model can be retrained independently of the OntoBDC code.
*   **Portability:** The mapping file allows different NLU models (or even different engines like OpenAI/LLMs) to map to the same Capabilities.
*   **Licensing Compliance:** OntoBDC is licensed under **Apache 2.0**, while Rasa (Open Source) is licensed under **GPLv3**. Embedding Rasa directly could force OntoBDC to adopt GPLv3 (viral effect). By keeping them as separate services communicating via API, we avoid this license conflict and maintain the permissive nature of the OntoBDC core.
