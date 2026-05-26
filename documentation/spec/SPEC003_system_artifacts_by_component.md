# SPEC 003 - System Artifacts By Component

## Status

- **Status**: Working specification of the current system artifacts
- **Scope**: OntoBDC core components and their respective artifacts
- **Primary sources**:
  - `wip/src/ontobdc`
  - `docs/documentation/spec/SPEC001_core_modules_and_commands.md`
  - `docs/documentation/spec/SPEC004_component_flows/README.md`

## 1. Purpose

This specification describes the main artifacts handled by each OntoBDC core component.

In this document, an artifact means any of the following:

- a persistent file written by the system
- a structured file read as configuration or metadata
- a runtime output artifact intentionally exposed to the user
- a static reference asset used by a component during execution

The goal is to answer:

- which artifacts belong to each component
- which artifacts are persisted versus operational
- which artifacts are inputs, outputs, or reference assets
- how artifacts relate across components

## 2. Artifact Categories

The current core uses four practical artifact categories.

### 2.1 Persistent Runtime Artifacts

These are created or updated during execution and remain on disk.

Examples:

- `.__ontobdc__/config.yaml`
- `.__ontobdc__/storage.rdf`
- A3 lifecycle package files such as `raw.txt` and `event.jsonld`

### 2.2 Configuration Artifacts

These control behavior or declare component state.

Examples:

- `check/config.json`
- `.__ontobdc__/config.yaml`

### 2.3 Reference Artifacts

These are static files used as execution references.

Examples:

- `a3/domain/machine/standard_a3_extraction.yaml`
- shell wrappers such as `message_box.sh`
- ontology and capability metadata loaded by plugins

### 2.4 Runtime Presentation Artifacts

These are not typically persisted, but they are still system outputs.

Examples:

- Rich terminal cards
- JSON output from `list` or `storage --json`
- success and error message boxes

## 3. Component Artifact Matrix

| Component | Main persistent artifacts | Main configuration/reference artifacts | Main operational outputs |
|---|---|---|---|
| `init` | `.__ontobdc__/config.yaml` | `check/config.json`, `message_box.sh`, `print_log.sh` | initialization messages |
| `check` | none by default, except when repair actions modify environment | `check/config.json`, `check/infra/*/init.sh` | check summaries and repair feedback |
| `run` | no standard persistent artifact by default | capability packages, parameter strategy files, renderers | capability results, rich output, JSON export |
| `list` | no standard persistent artifact | capability packages and metadata loaders | rich capability catalog or JSON catalog |
| `storage` | `.__ontobdc__/storage.rdf`, local dataset structure under storage roots | storage adapters and repository abstractions | dataset list, JSON storage view, registration/removal feedback |
| `dev` | updates inside `.__ontobdc__/config.yaml`; repository state changes in Git workspaces | `branch.sh`, `commit.sh`, `help.sh` | dev workflow messages, branch/commit feedback |
| `a3` | lifecycle package artifacts such as `raw.txt`, `parsed.json`, `graph.ttl`, `event.jsonld`, `err.json`; A3 log files | `standard_a3_extraction.yaml`, A3 capability plugins | ETL/work success and failure messages |
| `shared` | none directly as a primary owner | reusable adapters, repository contracts, logger contracts, ontology utilities | internal support behavior |
| `module` | capability-owned outputs when executed through `run` | packaged capabilities, templates, renderers | capability-specific outputs |

## 4. Component Specifications

### 4.1 `init` Component Artifacts

#### Primary Persistent Artifacts

- `.__ontobdc__/config.yaml`
  - local project configuration
  - stores execution engine and component configuration

#### Reference Artifacts

- `check/config.json`
  - used to validate allowed engine values
- `cli/message_box.sh`
- `cli/print_log.sh`

#### Role

The `init` component owns the bootstrap artifacts that make the remaining core components possible.

### 4.2 `check` Component Artifacts

#### Primary Configuration Artifacts

- `check/config.json`
  - declares engine-aware and base check configuration
- `check/infra/*/init.sh`
  - shell-based check implementations

#### Persistent Artifacts

- no single standard repository artifact is written by `check` itself
- however, repair flows may indirectly change:
  - installed dependencies
  - local environment state

#### Operational Outputs

- terminal summaries
- compact check results
- repair feedback

#### Role

The `check` component is mostly an evaluator of existing artifacts and environment state rather than a producer of persistent files.

### 4.3 `run` Component Artifacts

#### Reference Artifacts

- capability packages loaded from configured capability namespaces
- parameter strategy files under `run/plugin/parameter`
- renderers and selectors under `run/adapter`

#### Persistent Artifacts

- no default component-owned persisted file

Important nuance:

- the `run` component itself does not define one universal persisted artifact
- instead, it delegates execution to capabilities, which may create their own outputs

#### Operational Outputs

- rendered terminal output
- structured JSON export
- capability-specific action results

#### Role

`run` is an execution broker. Its primary artifacts are runtime context, resolved capability metadata, and delegated outputs rather than a single storage file.

### 4.4 `list` Component Artifacts

#### Reference Artifacts

- capability classes and their `METADATA`
- catalog rendering helpers

#### Persistent Artifacts

- none by default

#### Operational Outputs

- rich capability cards
- JSON capability catalog

#### Role

`list` turns capability metadata into a discoverability artifact for the user, but it does not normally persist that catalog.

### 4.5 `storage` Component Artifacts

#### Primary Persistent Artifacts

- `.__ontobdc__/storage.rdf`
  - root storage index
  - stores registered dataset/container information

#### Dataset-Level Artifacts

The current core `storage` flow does not guarantee creation of a RO-Crate artifact as part of dataset registration.

Storage registration is centered on updating:

- `.__ontobdc__/storage.rdf`

and on validating or resolving dataset roots rather than materializing a RO-Crate structure inside the dataset.

#### Reference Artifacts

- repository adapters under `storage/adapter`
- source and render helpers

#### Operational Outputs

- list of registered datasets
- JSON storage view
- success and error messages for `--local`, `--remove`, and related operations

#### Role

The `storage` component is the main owner of persistent repository-level dataset indexing.

### 4.6 `dev` Component Artifacts

#### Primary Persistent Artifacts

- `.__ontobdc__/config.yaml`
  - updated with:
    - `dev.tool: enabled`
    - SSH key configuration such as `dev.repo.ssh.key_path`

#### External Workspace Artifacts

The `dev` component also changes repository state outside OntoBDC-owned metadata, such as:

- Git commits
- branch creation
- branch checkout state

These are valid system effects, even though they are not stored in an OntoBDC-specific file format.

#### Reference Artifacts

- `dev/branch.sh`
- `dev/commit.sh`
- `dev/help.sh`

#### Operational Outputs

- dev tool enablement messages
- branch status summaries
- commit workflow feedback

#### Role

The `dev` component owns configuration mutations plus repository state transitions in contributor workflows.

### 4.7 `a3` Component Artifacts

#### Primary Lifecycle Directory

The `a3` component persists its runtime state in lifecycle package directories under the configured lifecycle root.

#### Lifecycle Package Artifacts

The current lifecycle sequence uses these file artifacts:

- `raw.txt`
  - received source content
- `sanitized.txt`
  - cleaned text artifact
- `parsed.json`
  - structured extracted data
- `graph.ttl`
  - translated RDF graph
- `validated.txt`
  - validation report artifact
- `reasoned.ttl`
  - reasoning-stage artifact
- `event.jsonld`
  - final dispatched event
- `err.json`
  - failure artifact for error reporting

#### Logging Artifacts

- `.__ontobdc__/log/a3/a3_pipeline_<YYYY-MM-DD>.log`
  - A3 pipeline execution log with daily rotation

#### Reference Artifacts

- `a3/domain/machine/standard_a3_extraction.yaml`
  - canonical statechart definition
- A3 capability implementations under `a3/plugin/capability`

#### Role

The `a3` component is the richest artifact-producing component in the current core. It externalizes its state almost entirely through physical files.

### 4.8 `shared` Component Artifacts

#### Primary Role

`shared` is not a primary artifact owner in the same sense as `storage` or `a3`.

Its main artifacts are reusable support assets:

- ontology access utilities
- plugin-loading utilities
- repository and logger contracts
- generic parameter abstractions

#### Persistent Artifacts

- none as a first-class component-owned output

#### Role

`shared` defines common technical artifacts that other components depend on structurally.

### 4.9 `module` Component Artifacts

#### Primary Role

The `module` package contains packaged capabilities and templates that participate in execution through `run`.

#### Reference Artifacts

- capability implementations
- capability metadata
- template renderers such as cards and tables

#### Persistent Artifacts

- no single universal artifact owned by the package itself
- outputs depend on the executed capability

#### Role

`module` is a provider of reusable execution artifacts rather than a single artifact-producing component.

## 5. Cross-Component Artifact Relationships

### 5.1 Bootstrap Dependency

- `init` creates `config.yaml`
- `check`, `run`, `storage`, `dev`, and `a3` depend on that artifact for normal operation

### 5.2 Dataset Metadata Dependency

- `storage` maintains `storage.rdf`
- `a3` and dataset-oriented workflows rely on registered dataset structure and repository abstractions built on top of that model

### 5.3 Capability Metadata Dependency

- `list` and `run` both rely on capability metadata artifacts

### 5.4 File-Driven State Dependency

- `a3` evaluates state from the physical presence of files
- this makes A3 artifacts both outputs and state indicators

## 6. Design Characterization

The current system uses two major artifact styles:

- metadata-oriented artifacts
  - such as `config.yaml` and `storage.rdf`
- lifecycle-oriented artifacts
  - such as `raw.txt`, `parsed.json`, `graph.ttl`, and `event.jsonld`

This reflects a broader architectural pattern in OntoBDC:

- configuration is persisted explicitly
- package state is often expressed through files
- many runtime outputs are intentionally human-readable or easy to manipulate

## 7. Summary

The OntoBDC core does not revolve around a single artifact type. Instead, each component owns a different artifact profile.

The most important current artifact owners are:

- `init`
  - for bootstrap configuration
- `storage`
  - for dataset index metadata
- `a3`
  - for lifecycle package artifacts
- `dev`
  - for local developer configuration and repository state changes

Components such as `run` and `list` are more output-oriented than file-oriented, while `shared` and `module` mostly provide support and reusable reference assets.

Overall, the current artifact design is layered, component-specific, and strongly oriented toward explicit files that remain understandable and manipulable outside the runtime itself.
