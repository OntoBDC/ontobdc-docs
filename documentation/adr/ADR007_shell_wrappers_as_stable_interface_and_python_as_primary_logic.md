# ADR 007: Use Shell Wrappers As A Stable Operational Interface And Python As The Primary Logic Layer

## Status

Accepted

## Context

The OntoBDC core exposes a CLI surface that needs to remain operational across different execution contexts, including:

- local source execution
- initialized project workflows
- script delegation between components
- terminal-oriented user interaction

At the same time, the system contains logic that is better expressed in Python, especially when dealing with:

- structured configuration
- capability discovery
- metadata normalization
- context resolution
- repository abstractions
- domain-oriented execution flows

This creates a recurring architectural question:

- should commands be implemented primarily as shell scripts or primarily as Python modules?

The current codebase already reflects a hybrid pattern.

In practice:

- shell scripts provide the operational command wrappers
- Python modules provide most of the structured and reusable runtime logic

Examples of this pattern include:

- shell-based command entry scripts under component directories
- Python entrypoints and helpers for configuration, discovery, and execution
- shell wrappers delegating to Python when structured logic is needed
- Python entrypoints delegating to shell scripts when the operational interface is script-oriented

Without a clear decision, the project risks drifting into inconsistent command design, such as:

- duplicating business logic in shell
- scattering operational glue across unrelated Python modules
- mixing terminal presentation concerns with domain logic
- making CLI behavior harder to test and harder to evolve consistently

This recurring design pattern should therefore be recorded explicitly.

## Decision

OntoBDC adopts the following command-layer split:

- shell wrappers are the stable operational interface for command entry and script delegation
- Python modules are the primary layer for structured logic, domain behavior, and reusable runtime services

### Shell Wrappers

Shell wrappers are the preferred boundary for:

- command invocation glue
- delegation between scripts and subcommands
- environment-aware command launching
- terminal-facing orchestration
- lightweight operational prechecks

Their role is to behave as the stable operational interface of the system.

They are allowed to:

- collect and forward arguments
- resolve script-relative paths
- call shared shell presentation utilities
- invoke Python helpers when structured processing is required
- coordinate external tools such as Git or Bash-based infra routines

They should not become the main place for complex structured business logic when Python is a better fit.

### Python Modules

Python is the primary implementation layer for:

- configuration loading and mutation
- metadata parsing
- capability discovery
- CLI context resolution
- repository abstractions
- domain-oriented workflows
- reusable helper logic shared across components

Python modules are preferred when the behavior requires:

- structured data handling
- reuse across commands or components
- richer validation
- extension through ports, adapters, loaders, and strategies

### Interaction Pattern

This decision does not require a one-way architecture.

Two interaction patterns are valid:

- shell wrapper calling Python for structured logic
- Python CLI entrypoint delegating to shell wrapper for operational command execution

What matters is the responsibility boundary:

- shell remains the stable operational shell
- Python remains the primary home of structured logic

## Rationale

This decision exists to preserve four important properties of the command architecture:

- operational stability
- maintainability
- clarity of responsibility
- testability

### Operational Stability

Shell wrappers are well suited to command dispatch and system orchestration tasks.

They provide a stable integration surface for:

- invoking companion scripts
- launching checks
- forwarding arguments
- interacting with the terminal environment

This keeps the operational command surface simple and explicit.

### Maintainability

Structured runtime logic becomes difficult to maintain when written directly in shell.

Python provides a better foundation for:

- configuration structures
- metadata models
- plugin loading
- context pipelines
- reusable abstractions

Keeping this logic in Python reduces duplication and makes refactoring safer.

### Clarity Of Responsibility

The split prevents shell scripts from becoming ad hoc business logic containers and prevents Python modules from being overloaded with operational wrapper concerns.

This makes the system easier to reason about:

- shell handles command orchestration
- Python handles logic and structure

### Testability

The hybrid design supports multiple useful testing layers:

- shell tests for command surface and integration behavior
- Python tests for internal logic and domain behavior

This division is harder to preserve if commands are implemented entirely in one layer without regard for responsibility boundaries.

## Consequences

### Positive

- command entry behavior remains explicit and operationally stable
- structured logic stays in a language better suited for it
- configuration and metadata behavior become easier to reuse and test
- CLI integration tests can focus on wrappers while Python tests focus on internals
- components can evolve without rewriting every command as either pure shell or pure Python

### Negative

- contributors must navigate two implementation layers instead of one
- some flows require tracing shell-to-Python or Python-to-shell delegation
- poor discipline could still lead to duplication if the boundary is not respected

### Neutral

- this decision does not require every small command to use both layers
- some commands may remain thinner on one side depending on their role
- the architecture is layered by responsibility, not by forcing symmetry in every component

## Alternatives Considered

### Pure Shell Command Architecture

Rejected because structured logic such as metadata parsing, context resolution, and plugin-oriented behavior becomes harder to maintain and test in shell.

### Pure Python Command Architecture

Rejected because the project already benefits from shell-based operational wrappers for command orchestration, environment-aware launching, and script-level delegation.

### No Stable Pattern, Decide Per File

Rejected because it encourages drift, duplication, and unclear ownership between operational glue and business logic.

## Implementation Notes

The current repository reflects this decision through patterns such as:

- shell command wrappers under component directories
- Python runtime logic in modules such as:
  - `cli`
  - `run`
  - `storage`
  - `a3`
  - `dev`
- shared shell presentation scripts such as message box and logging helpers
- shell tests for entrypoint behavior
- Python tests for structured runtime behavior

This ADR should be read together with:

- [SPEC001_core_modules_and_commands.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC001_core_modules_and_commands.md)
- [ADR001_dependency_injection_and_components_extras_split.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/adr/ADR001_dependency_injection_and_components_extras_split.md)

## Future Direction

This decision supports future work such as:

- moving duplicated structured shell logic into Python helpers
- keeping shell wrappers thin and operationally focused
- strengthening test coverage separately for wrappers and core logic
- clarifying component-by-component boundaries when old command implementations are refactored
