---
title: "OntoBDC Whitepaper 2026"
subtitle: "Capability-Driven Runtime for Composable Semantic Data Workflows"
version: "0.6.0"
date: "2026-03-14"
status: "draft"
---

# Abstract

OntoBDC is a capability-driven runtime for building reproducible, inspectable, and composable data workflows. Instead of hardcoding pipelines as fixed directed graphs, OntoBDC treats operations as discoverable Capabilities with explicit input/output contracts and semantic metadata. Users and tools can query what operations exist, what they require, what they produce, and how they can be composed. The OntoBDC CLI provides consistent discovery and execution interfaces (`list`, `run`, `init`), and a context layer that can materialize provenance artifacts (e.g., RO-Crate) in a standardized hidden workspace. This whitepaper introduces the Capability model, outlines the execution architecture and planning approach, and provides guidance for adopting Capabilities in data curation and knowledge workflows.

# 1. Introduction

## 1.1 Motivation

Modern data curation projects frequently degrade into collections of scripts with hidden assumptions:

- Dependencies are implicit (a file is assumed to exist, a folder is assumed to be “the root”).
- Execution environments drift (local laptop vs. CI vs. notebooks).
- Provenance is incomplete (what inputs, parameters, versions produced an artifact?).
- Reuse is limited (operations are entangled with paths and orchestration glue).

OntoBDC addresses these issues by elevating the unit of reuse and governance: the Capability.

## 1.2 Goals

- Define Capabilities as explicit execution units with stable identifiers and semantic versioning.
- Provide runtime discovery: “What can be done here?” and “What can be done with this data?”
- Enable dynamic composition through explicit I/O contracts and semantic types.
- Provide a consistent CLI interface for listing, selecting, and executing capabilities.
- Capture context and provenance as first-class artifacts (e.g., RO-Crate) in a predictable location.

## 1.3 Non-Goals

- OntoBDC is not a replacement for orchestration platforms; it can complement them with stronger domain-level modularity.
- OntoBDC does not attempt to define a universal ontology; it uses semantic identifiers and contracts to support executable semantics and traceability.

# 2. Problem Statement

## 2.1 Rigid Workflow Definition

Traditional pipeline tools (e.g., Airflow, Luigi, Prefect, Dagster) are effective for scheduling and orchestration, but they typically require workflows to be defined explicitly as code. This leads to:

- Hardcoded pipelines that are expensive to refactor.
- Limited operation reuse outside of the original DAG context.
- Low discoverability of available operations for a given dataset.

## 2.2 Coupling Between Data and Execution

Many systems couple:

- workflow logic (what steps exist)
- data location (paths, buckets, database names)
- environment assumptions (tools, engines, credentials)

Consequences include brittle automation and low dataset portability.

## 2.3 Limited Operation Discovery

Teams often cannot answer, reliably and programmatically:

- What operations are available in this environment?
- Which operations are compatible with the artifacts I have?
- What operations can produce the missing inputs for a target operation?

OntoBDC is designed to make these questions first-class.

# 3. Core Concepts

## 3.1 Capability

A Capability is a discoverable, versioned unit of behavior that declares explicit contracts:

- **Identifier**: a globally unique ID (URI-like string).
- **Version**: semantic version.
- **Description**: human-readable intent.
- **Inputs**: typed parameters (required/optional) with semantic bindings.
- **Outputs**: typed results with semantic bindings.
- **Actions (optional)**: explicit side effects that must be triggered intentionally.

Capabilities are designed to be:

- **Composable**: chained by matching outputs to required inputs.
- **Inspectable**: metadata is available through CLI and machine export.
- **Portable**: the same Capability can run in different contexts with consistent semantics.

## 3.2 Capability Metadata Model

Minimum metadata required for reliable discovery and composition:

- `id`: stable, globally unique identifier.
- `version`: semantic version.
- `description`: intent and scope.
- `inputs`: list of parameters, their types, requirements, and semantic URIs.
- `outputs`: list of results, their types, and semantic URIs.

Operational metadata commonly included:

- origin (module/package) for discovery
- runtime constraints (engine/environment requirements)
- context binding URIs for traceability

## 3.3 Actions

Actions represent optional, explicit side effects associated with a run (e.g., exporting, writing, publishing). They should be:

- enumerated and discoverable
- invoked deliberately (not implicitly)
- recorded in run context/provenance artifacts

## 3.4 Context

Context is the structured record of “what happened”:

- what was executed (Capability ID/version)
- which inputs/parameters were used
- what outputs were produced
- which files were read/written (when applicable)
- which engine/environment was used

OntoBDC standardizes a hidden directory for operational state and provenance artifacts:

- `.__ontobdc__/`

# 4. System Overview

## 4.1 High-Level Architecture

At a conceptual level, OntoBDC separates:

- **Capability runtime**: discovery, selection, execution, export.
- **Repository abstraction**: ports + adapters that access documents/datasets.
- **Context/provenance layer**: records and materializes context artifacts (e.g., RO-Crate).

Typical flow:

1. Discover available capabilities.
2. Choose a capability (interactive or scripted).
3. Resolve its required inputs from repositories and user parameters.
4. Execute the capability and capture context.
5. Optionally materialize provenance artifacts.

## 4.2 Repository Abstraction (Ports and Adapters)

Capabilities depend on repository ports (interfaces), not concrete storage:

- Document repositories
- Dataset repositories

Adapters implement those ports for concrete backends such as local folders. This enables:

- unit testing with mock repositories
- portability across environments and storage backends
- consistent inspection and export behaviors

# 5. Capability Model (Detailed)

## 5.1 Definition

A Capability can be seen as:

**Executable operation** + **semantic metadata** + **input/output contracts**

## 5.2 Inputs and Outputs as Contracts

Contracts connect capabilities:

- Capability A produces output type **X**.
- Capability B requires input type **X**.

This defines compatibility and supports composition. Contracts can be strengthened by:

- semantic URIs to remove ambiguity
- explicit parameter requirements (required/optional)
- stable IDs for outputs that can be referenced across tooling

## 5.3 Capability Graph

The set of installed capabilities can be represented as a directed graph:

- **Nodes**: capabilities
- **Edges**: “can satisfy” relationships based on output → input compatibility

This capability graph enables:

- dependency discovery
- plan construction for a target capability
- “next-step suggestions” after a run (based on produced outputs)

# 6. Execution and Planning

## 6.1 Strategy-Based CLI Pipeline

OntoBDC CLI execution can be modeled as a pipeline of strategies:

1. Parse CLI args into a context object.
2. Apply strategies (help, export mode, filtering, pagination, selection).
3. Execute the selected capability.
4. Export results (human or machine output).

This design improves extensibility: new behaviors can be added as strategies without rewriting the entire CLI.

## 6.2 Execution Planning (Capability-Driven)

When a user requests a capability:

1. The runtime determines required inputs.
2. It searches for existing data or prior outputs that satisfy them.
3. If missing, it can identify which capabilities could produce required inputs.
4. A plan (DAG) can be constructed dynamically.

The key distinction is that pipelines are **inferred** from contracts and available data rather than being fully hardcoded.

# 7. CLI Interaction Model

## 7.1 Discovering Capabilities

`ontobdc list` supports:

- rich, interactive-friendly output for humans
- `--json` output for automation and integration

This makes metadata inspection a first-class workflow, not a side effect of reading source code.

## 7.2 Running Capabilities

`ontobdc run` supports:

- interactive selection of capabilities
- parameter resolution and validation
- consistent run output and error reporting

## 7.3 Initialization and Context

`ontobdc init` prepares local operational state:

- creates `.__ontobdc__/`
- writes baseline configuration (`.__ontobdc__/config.yaml`)
- selects an engine profile (e.g., venv vs. colab)

`ontobdc init context` (context materialization):

- creates a RO-Crate metadata file in `./.__ontobdc__/ro-crate-metadata.json`
- prompts the user with an explicit confirmation (shows the target path)

# 8. Governance and Versioning

## 8.1 Semantic Versioning

Capabilities follow SemVer:

- **MAJOR**: breaking changes to I/O contracts or behavior
- **MINOR**: backward-compatible additions
- **PATCH**: fixes and internal improvements

## 8.2 Identifier Stability

- capability IDs should remain stable across versions
- deprecations should be explicit and discoverable through metadata and release notes

# 9. Comparison with Existing Systems (High-Level)

| System | Workflow Defined as DAG | Semantic I/O Contracts | Automatic Composition |
|---|---:|---:|---:|
| Airflow | Yes | No | No |
| Prefect | Yes | No | No |
| Dagster | Yes | Partial | No |
| OntoBDC | No (inferred) | Yes | Yes (planned / incremental) |

# 10. Example Use Case (Illustrative)

Consider a dataset containing an exported WhatsApp archive. Available capabilities might include:

- list input archives
- extract messages into a structured representation
- compute statistics
- generate a report

Rather than requiring a pre-wired pipeline, OntoBDC can:

1. Discover capabilities compatible with the available artifacts.
2. Execute a target capability (e.g., “compute statistics”).
3. Infer required steps from contracts (e.g., extraction must precede statistics).
4. Record outputs and context artifacts for reproducibility.

# 11. Extensibility

OntoBDC supports extensibility through modular capability packages:

- add new capability implementations without changing the core runtime
- register metadata for discovery and inspection
- implement additional repository adapters for new storage backends

# 12. Roadmap (Draft)

- Capability graphs and dependency resolution integrated into the CLI (plan/inspect).
- Standard export targets (JSON, RO-Crate enrichment, reports).
- Capability-level caching and incremental execution.
- Repository adapters for cloud storage and databases.
- Assisted planning (interactive suggestions, tool-assisted composition).

# 13. Conclusion

OntoBDC proposes Capabilities as a practical unit for reusable, discoverable, semantically grounded operations in data curation workflows. By making contracts explicit and context a first-class artifact, OntoBDC improves reproducibility and portability while enabling dynamic composition. The result is an execution model that supports both exploratory usage and systematic automation without requiring every workflow to be hardcoded upfront.

# Appendix A: Terminology

- **Capability**: discoverable, versioned unit of behavior with explicit I/O contracts
- **Action**: explicit side effect associated with a capability execution
- **Context**: structured record of execution intent and outcomes
- **Repository (Port/Adapter)**: abstraction for accessing documents/datasets
- **Engine**: runtime mode (venv/colab/others)

# Appendix B: Suggested References

- RO-Crate specification
- Data Package specification
- Semantic Versioning (SemVer)
