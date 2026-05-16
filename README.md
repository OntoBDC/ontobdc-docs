# OntoBDC

OntoBDC is a Python CLI and semantic runtime for defining, discovering, validating, and executing capability-based workflows over structured data and semantic context.

It focuses on making workflows more predictable and auditable by combining explicit capability metadata, schema-driven inputs/outputs, and verification steps (e.g., checks, contracts, storage indexing) around execution.

## Documentation

- Use Cases: [documentation/use_case/README.md](documentation/use_case/README.md)

## Quickstart

1. Initialize a project context:
   - `ontobdc init`
2. Validate environment and configuration:
   - `ontobdc check`
3. Discover what is available:
   - `ontobdc list`
4. Execute a capability:
   - `ontobdc run <capability_id> [args]`
5. Manage the storage index:
   - `ontobdc storage`
   - `ontobdc storage --local [path]`
   - `ontobdc storage --remove <dataset_id>`

## What OntoBDC Does

- Creates and maintains a per-project configuration in `.__ontobdc__/config.yaml`.
- Runs pre-flight checks to reduce environment drift before execution.
- Discovers installed capabilities and exposes them through a consistent CLI.
- Executes capabilities using declared schemas and runtime strategies.
- Maintains a storage index (`.__ontobdc__/storage.rdf`) that references dataset locations.
- Supports workflows in domains that benefit from explicit contracts and auditability (e.g., BIM/openBIM, engineering data, compliance-oriented pipelines).

## Architecture

The diagrams below summarize the system context (C1) and the internal CLI containers (C2).

### C1 - System Context

```mermaid
flowchart LR
  User["User<br/>(Dev / Data Scientist)"]
  System["OntoBDC CLI<br/>(System)"]

  Project["OntoBDC Project<br/>(working directory)"]
  Config["Project Config<br/>(.__ontobdc__/config.yaml)"]
  StorageIndex["Storage Index<br/>(.__ontobdc__/storage.rdf)"]
  Datasets["Local Datasets<br/>(storage paths)"]
  Python["Python Runtime<br/>(venv/colab/docker)"]
  Git["Git Repository"]
  Internet["Internet / External Data Sources"]

  User -->|"runs commands"| System

  System -->|"operates in"| Project
  System -->|"uses"| Python
  System -->|"reads/writes"| Config
  System -->|"reads/writes"| StorageIndex
  StorageIndex -->|"references"| Datasets
  System -->|"invokes"| Git
  System -->|"accesses"| Internet
```

### C2 - Container Diagram

```mermaid
flowchart LR
  User["User"]

  subgraph OntoBDC["OntoBDC CLI (System)"]
    CLI["CLI Entrypoints<br/>(ontobdc)"]
    Init["Init Use Case<br/>(init)"]
    Check["Check Use Case<br/>(check)"]
    Run["Run Use Case<br/>(run)"]
    List["List Use Case<br/>(list)"]
    Storage["Storage Use Case<br/>(storage)"]
    Dev["Dev Use Case<br/>(dev)"]
    Runtime["Capability Runtime<br/>(loader + strategies)"]
  end

  Config[".__ontobdc__/config.yaml"]
  StorageIndex[".__ontobdc__/storage.rdf"]
  Datasets["Local Datasets"]
  Capabilities["Installed Capability Modules<br/>(Python packages)"]
  Git["Git"]
  Internet["Internet"]

  User --> CLI

  CLI --> Init
  CLI --> Check
  CLI --> Run
  CLI --> List
  CLI --> Storage
  CLI --> Dev

  Init --> Config
  Check --> Config
  Run --> Runtime
  Runtime --> Config
  Runtime --> Capabilities
  Runtime --> Internet
  List --> Capabilities
  Storage --> StorageIndex
  StorageIndex --> Datasets
  Dev --> Git
```

## Core Concepts (Mental Model)

- Project Context: the `.__ontobdc__` folder that stores project state and metadata.
- Capability: an executable unit with explicit metadata, inputs, and outputs.
- Checks: deterministic validations to ensure the environment and prerequisites are correct before execution.
- Storage Index: an RDF index that registers dataset locations and enables repeatable references.

## Status

OntoBDC is under active development. The CLI is usable, but capabilities and workflows evolve quickly as the project expands its domain coverage and validation strategy.
