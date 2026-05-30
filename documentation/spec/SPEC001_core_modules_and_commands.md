# SPEC 001 - OntoBDC Core Modules And Commands

## Status

- **Status**: Working specification of the current core CLI surface
- **Scope**: `wip/src/ontobdc`
- **Audience**: maintainers, contributors, and users of the OntoBDC core distribution

## 1. Purpose

This specification describes the current OntoBDC core modules, their exposed commands, their options, and their operational roles.

The focus is the command surface currently wired by the main CLI entrypoint and the core modules that support it.

This document answers:

- which core modules exist
- which of them expose user-facing commands
- which options are currently accepted
- what each command is expected to do
- which commands are conditional or gated by configuration

## 2. Source Of Truth

This specification is derived from the current code under:

- `wip/src/ontobdc/cli`
- `wip/src/ontobdc/check`
- `wip/src/ontobdc/run`
- `wip/src/ontobdc/list`
- `wip/src/ontobdc/storage`
- `wip/src/ontobdc/dev`
- `wip/src/ontobdc/a3`
- `wip/src/ontobdc/shared`
- `wip/src/ontobdc/module`

The top-level command routing is defined in:

- `wip/src/ontobdc/cli/__init__.py`

## 3. Core Component Overview

The current core package is organized around these functional modules:

- `cli`
  - top-level command routing
  - initialization helpers
  - shared CLI presentation utilities
- `check`
  - infrastructure and environment validation
- `run`
  - capability discovery, filtering, selection, and execution
- `list`
  - capability listing and metadata rendering
- `storage`
  - dataset registration and storage index management
- `dev`
  - multi-repository developer workflows
- `a3`
  - A3-oriented ETL and work execution
- `shared`
  - shared adapters and ports used across modules
- `module`
  - built-in capability modules and templates used by the execution layer

From a user-facing CLI perspective, the currently exposed top-level commands are:

- `ontobdc init`
- `ontobdc check`
- `ontobdc run`
- `ontobdc list`
- `ontobdc storage`
- `ontobdc dev`
- `ontobdc a3`

The CLI also exposes:

- `ontobdc help`
- `ontobdc version`

## 4. Global Command Behavior

The main command behavior is currently:

- `ontobdc init` can run before initialization
- all other routed commands require a valid `.__ontobdc__/config.yaml`
- `ontobdc dev` requires `dev.tool: enabled` for most operations
- `ontobdc a3` requires the A3 module to be enabled in the current environment

The CLI determines project root primarily from:

- `ONTOBDC_PROJECT_ROOT`
- or upward search for `.__ontobdc__/config.yaml`

## 5. Command Matrix

| Module | Top-level command | Role | Availability |
|---|---|---|---|
| `cli.init` | `ontobdc init` | Initialize local project configuration | always available |
| `check` | `ontobdc check` | Validate operational environment | requires initialized project |
| `run` | `ontobdc run` | Discover and execute capabilities | requires initialized project |
| `list` | `ontobdc list` | List available capabilities | requires initialized project |
| `storage` | `ontobdc storage` | Manage storage index and local datasets | requires initialized project |
| `dev` | `ontobdc dev` | Developer workflows across repos | requires initialized project and usually `dev.tool` enabled |
| `a3` | `ontobdc a3` | A3 ETL and work tools | requires initialized project and A3 enabled |

## 6. Module Specifications

### 6.1 `cli` / `ontobdc init`

#### Purpose

The `init` command is the initialization entrypoint of OntoBDC for local project configuration.

#### Commands

- `ontobdc init [engine]`

#### Options And Arguments

- positional `engine`
  - accepted values are validated against `check/config.json`
  - current intended examples include `venv` and `colab`
  - if omitted, the CLI tries to auto-detect:
    - `colab` when `/content` exists
    - `venv` when a virtual environment is active

#### Behavior

- creates `.__ontobdc__/config.yaml`
- writes the selected execution engine
- attempts to run repair-oriented checks after engine initialization
- blocks duplicate initialization when config already exists

#### Description

This module establishes the minimum local structure required by the rest of the CLI.

### 6.2 `check` / `ontobdc check`

#### Purpose

The `check` module validates whether the current project and environment are operational.

#### Command

- `ontobdc check [options]`

#### Options

- `--repair`
  - attempts repair actions when available
- `--scope <name>`
  - restricts checks to a named scope
- `--only <check>`
  - runs only a single named check
- `--ignore-warnings`
  - suppresses warning emphasis in summary behavior
- `-c`, `--compact`
  - uses compact output

#### Behavior

- resolves engine from `.__ontobdc__/config.yaml`
- loads check configuration from `check/config.json`
- runs base and engine-aware checks
- supports fatal and recoverable checks
- may invoke `repair` or `hotfix` functions defined by check scripts

#### Description

`check` is the operational gatekeeper of the core system. It is used both directly and as part of initialization and developer workflows.

### 6.3 `run` / `ontobdc run`

#### Purpose

The `run` module is the execution entrypoint for OntoBDC capabilities.

It performs:

- CLI context resolution
- parameter extraction
- capability discovery
- capability filtering
- interactive selection when needed
- execution and rendering

#### Command

- `ontobdc run [options]`

#### Core Options

- `--id <ID>`
  - targets a specific capability by ID
- `--help`, `-h`
  - shows help
- `--root-path <PATH>`
  - sets the root repository path
- `--repository <PATH>`
  - alias-like input for repository path resolution
- `--limit <N>`
  - pagination limit
- `--start <N>`
  - pagination start offset
- `--file-name <PATTERN>`
  - filters by file name
- `--file-type <EXT[,EXT...]>`
  - filters by one or more file types
- `--text-file <PATH>`
  - injects a raw text file path into context
- `--export <json|rich>`
  - selects renderer output format
- `--action-only`
  - limits execution intent to action output only
- `-a`, `-auc`, `-uca`, `--all`
  - sets `include_action = true`

#### Behavior

- resolves built-in parameter strategies from `run/plugin/parameter`
- discovers capabilities through the plugin loader
- executes the targeted capability directly when `--id` is provided
- otherwise presents an interactive capability selector
- renders output through a capability-specific renderer when present

#### Description

`run` is the main programmable interface of the platform. It is intentionally extensible through capability plugins and CLI context strategies.

### 6.4 `list` / `ontobdc list`

#### Purpose

The `list` module exposes the currently discoverable capabilities and their metadata.

#### Command

- `ontobdc list [options]`

#### Options

- `--json`
  - outputs capability metadata as JSON
- `--help`, `-h`
  - shows help

#### Behavior

- loads capability metadata through the plugin loader
- deduplicates by capability ID
- renders either:
  - JSON
  - rich capability cards

#### Description

`list` is the catalog view of the capability ecosystem loaded by the core.

### 6.5 `storage` / `ontobdc storage`

#### Purpose

The `storage` module manages registered datasets and storage metadata.

#### Commands

- `ontobdc storage --list`
- `ontobdc storage --enable`
- `ontobdc storage --help`

#### Options

- `--list`, `-l`
  - lists all containers in the storage
- `--enable`
  - enables the storage component by installing dependencies and creating the storage index file
- `--help`, `-h`
  - shows help

#### Behavior

- lists current storage entries when `--list` is provided
- enables storage capabilities and creates `storage.rdf` when `--enable` is provided
- delegates operations to the corresponding Python command plugins:
  - `list.py`
  - `enable.py`
  - `base.py`

#### Description

`storage` is the dataset registration and storage-index module of the core.

### 6.6 `dev` / `ontobdc dev`

#### Purpose

The `dev` module provides developer-focused multi-repository operations and config helpers.

#### Command Family

- `ontobdc dev --help`
- `ontobdc dev --enable-dev-tool`
- `ontobdc dev commit "<message>"`
- `ontobdc dev branch`
- `ontobdc dev branch --create <name>`
- `ontobdc dev checkout <name>`
- `ontobdc dev changelog [target_ref]`
- `ontobdc dev repo --add-ssh-key <path>`
- `ontobdc dev repo --rm-ssh-key`

#### Options And Subcommands

- `--help`, `-h`
  - shows module help
- `--enable-dev-tool`
  - enables `dev.tool: enabled` in `.__ontobdc__/config.yaml`
  - must be passed alone
- `commit <message>`
  - stages, commits, and attempts push across repositories
- `branch`
  - shows git status across root repo and sub-repos
- `branch --create <name>`
  - creates and pushes a branch across repositories
- `branch --checkout <name>`
  - checks out an existing branch across repositories
- `checkout <name>`
  - alias for `branch --checkout <name>`
- `changelog [target_ref]`
  - compares the current branch against a base branch or target ref
- `repo --add-ssh-key <path>`
  - saves SSH key path into config
- `repo --rm-ssh-key`
  - removes SSH key path from config

#### Behavior

- runs `ontobdc check -c` before most operations
- requires `dev.tool: enabled` for normal dev workflow
- traverses root repo plus detected submodules and known sibling repos
- uses stored SSH key path when push requires explicit SSH identity

#### Description

`dev` is the repository orchestration module for contributors working on multi-repo OntoBDC workspaces.

### 6.7 `a3` / `ontobdc a3`

#### Purpose

The `a3` module exposes A3-specific ETL and work-processing tools.

#### Command Family

- `ontobdc a3 --etl --source <file|url>`
- `ontobdc a3 --work`
- `ontobdc a3 --help`

#### Options

- `--etl`
  - executes ETL flow
- `--source <file|url>`
  - required input for `--etl`
- `--work`
  - runs concurrent A3 work processing
- `--help`, `-h`
  - shows help

#### Availability

- the module checks whether A3 is enabled in the environment
- when disabled, it instructs the user to run:
  - `ontobdc extra --enable a3`

#### Description

`a3` is an optional but core-hosted workflow module for A3 data processing.

## 7. Internal Support Modules

These modules are part of the core but are not directly routed as top-level commands:

- `shared`
  - common adapters and ports for ontology, plugins, repository, and logging concerns
- `module`
  - packaged capability modules, such as `social` and `template`

They support the execution surface indirectly, especially through:

- capability loading
- adapter reuse
- domain-port contracts

## 8. Non-Routed Or Partially Exposed Elements

Some code exists in the core tree without being fully routed as first-class top-level commands.

Current examples:

- `cli/extra.py`
  - exists in the tree
  - not currently routed by `cli/__init__.py`

This means the current codebase contains more functionality than the strictly exposed top-level command list.

## 9. Command Availability Summary

### Always available before init

- `ontobdc init`
- `ontobdc help`
- `ontobdc version`

### Available after init

- `ontobdc check`
- `ontobdc run`
- `ontobdc list`
- `ontobdc storage`
- `ontobdc dev`
- `ontobdc a3`

### Additional gating

- `ontobdc dev`
  - usually requires `dev.tool: enabled`
- `ontobdc a3`
  - requires A3 enablement in the environment

## 10. Design Notes

The current OntoBDC core design shows a few consistent patterns:

- command routing is centralized in `cli/__init__.py`
- shell scripts are used as stable command wrappers
- Python modules hold most business logic
- execution is capability-oriented rather than command-hardcoded
- several commands are profile-aware and configuration-aware

This makes the core simultaneously:

- CLI-oriented
- plugin-oriented
- repository-oriented
- environment-sensitive

## 11. Summary

The OntoBDC core currently exposes a modular CLI centered on:

- initialization
- validation
- capability execution
- capability listing
- storage management
- developer workflows
- A3 workflows

The top-level core commands are:

- `init`
- `check`
- `run`
- `list`
- `storage`
- `dev`
- `a3`

Together, these modules define the current operational surface of the OntoBDC core distribution.
