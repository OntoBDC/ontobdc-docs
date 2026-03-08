---
code: SPEC004
title: RO-Crate Strategy (Modeling, Parsing, and Repository Abstraction)
status: Accepted
author: Elias M. P. Junior
date: 2026-03-08
tags: architecture, ro-crate, repository, parsing, modeling
---

# SPEC004: RO-Crate Strategy (Modeling, Parsing, and Repository Abstraction)

This document defines the unified strategy for **RO-Crate (Research Object Crate)** within the OntoBDC architecture. It covers modeling semantic data, repository abstraction constraints, and implementation details for both creating and consuming crates.

## 1. Context and Goals

OntoBDC uses RO-Crate (JSON-LD) as the **Layer 2 (Semantic)** standard to represent knowledge graphs, relationships, and provenance, independent of the **Layer 1 (Physical)** storage managed by Frictionless Data Packages.

| Layer | Standard | Responsibility | Entities Managed |
| :--- | :--- | :--- | :--- |
| **Layer 1 (Physical)** | Frictionless Data Package | File catalog, validation, types, paths. | `messages.json`, `threads.json`, `datapackage.json` |
| **Layer 2 (Semantic)** | RO-Crate (JSON-LD) | Knowledge Graph, relationships, provenance. | `Conversation`, `Thread`, `Task`, `Person`, `AIModel` |

## 2. Modeling Strategy (JSON-LD)

Entities are "lifted" from raw data into a Knowledge Graph using Schema.org vocabulary.

### 2.1 Core Entities

*   **Root Dataset**: Represents the main object of analysis (e.g., a WhatsApp Chat).
*   **Thread**: A logical grouping of messages (`CreativeWork` or `Conversation`).
*   **Task**: Extracted intents or actions (`Action` or `PlanAction`).
*   **Suggestion**: AI-generated content (`Comment` or `CreativeWork`).

### 2.2 Provenance
Provenance is critical. We explicitly state that an AI agent or specific process created the structure.

```json
{
  "@id": "#agent-gemini-pro",
  "@type": "SoftwareApplication",
  "name": "Gemini 1.5 Pro",
  "version": "1.5-pro-preview-0514"
}
```

## 3. Architecture Constraints: Repository Abstraction

OntoBDC strictly enforces access via `DocumentRepositoryPort` to support distributed and remote data sources.

### 3.1 The Constraint
**Capabilities MUST NEVER access the filesystem directly.** They MUST ALWAYS use a REPOSITORY.

### 3.2 Reading RO-Crates (Parsing)
Using the `ro-crate` library for **reading** often requires direct filesystem paths, which violates the abstraction.

**Decision:**
1.  **Repository-First Access**: Use `repository.get_json(path)` to retrieve metadata.
2.  **Manual/Lightweight Parsing**: Parse the JSON-LD graph manually (iterate over `@graph`) for simple filtering tasks.
3.  **Avoid `ro-crate` Library for Reading**: Do not use the library if it forces filesystem coupling.

### 3.3 Writing RO-Crates (Creation)
For **creating** complex RO-Crates, we **DO** use the `ro-crate` library, but wrapped within an **Adapter**.

**Decision:**
1.  **Use `ro-crate` Library**: The library is added as a dependency to handle the complexity of generating valid JSON-LD.
2.  **Adapter Pattern**: The `RoCrateDatasetAdapter` bridges the internal `DatasetRepositoryPort` and the library.

## 4. Implementation Details

### 4.1 Dependency
The `rocrate` library is included in `pyproject.toml`.

### 4.2 Metadata Storage Location
To avoid polluting the root directory of datasets, all OntoBDC-generated metadata files are stored in a hidden subdirectory: `.__ontobdc__/`.

*   **Data Package**: `.__ontobdc__/datapackage.json`
*   **RO-Crate**: `.__ontobdc__/ro-crate-metadata.json`

### 4.3 RoCrateDatasetAdapter Behavior
The adapter (`src/ontobdc/module/resource/adapter/crate.py`) implements specific logic to handle the coexistence of RO-Crates and Data Packages:

1.  **Initialization**: Creates a `ROCrate` instance.
2.  **Atomic Data Packages**: If a directory contains a Data Package (`.__ontobdc__/datapackage.json`), the adapter:
    *   Indexes **only** the `datapackage.json` file.
    *   **Excludes** all other files and subdirectories in that folder from the RO-Crate.
    *   This treats the Data Package as an atomic unit.
3.  **Standard Indexing**: For directories without a Data Package, it recursively indexes all files.
4.  **Exclusion**: Always excludes `.__ontobdc__` contents (except the targeted `datapackage.json`) and hidden files to prevent recursion loops.

### 4.4 Code Example (Creation)

```python
from ontobdc.module.resource.adapter.crate import RoCrateDatasetAdapter

# repo is a DatasetRepositoryPort
adapter = RoCrateDatasetAdapter(repository=repo)
# Generates .__ontobdc__/ro-crate-metadata.json
metadata = adapter.create_ro_crate(output_dir="/path/to/dataset")
```

### 4.5 Code Example (Reading/Parsing)

```python
# repo is a DocumentRepositoryPort
crate_path = "path/to/dataset/.__ontobdc__/ro-crate-metadata.json"
crate_content = repo.get_json(crate_path)

# Manual parsing compliant with repository abstraction
if crate_content and "@graph" in crate_content:
    for node in crate_content["@graph"]:
        if "urn:example:MyType" in node.get("@type", []):
            process_entity(node)
```
