# ADR 008: Introduce A Plugin-Based CLI Pre-Dispatch Layer With Structured Command Responses

## Status

Accepted

## Context

The OntoBDC CLI entrypoint in `wip/src/ontobdc/cli/__init__.py` historically relied on a monolithic command dispatch flow based on:

- raw `sys.argv` inspection
- a large `if` / `elif` command tree
- direct rendering side effects such as `print()`, `message_box.sh`, or shell delegation

That design has been operationally useful, but it creates several structural limitations:

- top-level CLI behavior is tightly coupled to one file
- command-specific parsing and rendering concerns accumulate inside the entrypoint
- introducing new command-like behaviors requires editing the central dispatcher
- root CLI flags such as `--help` do not have a first-class command abstraction
- command handlers do not return a stable response model that can be rendered consistently

At the same time, the project already uses plugin-oriented discovery successfully in other runtime layers, including:

- capability discovery
- parameter strategy discovery

The CLI is now evolving toward the same extensibility model.

The current codebase already contains the first working pieces of that transition:

- `CliCommandRunAdapter` in `wip/src/ontobdc/cli/adapter/command.py`
- `CliCommandPort` and `CliCommandMetadata` in `wip/src/ontobdc/cli/domain/port/command.py`
- structured response dataclasses in `wip/src/ontobdc/cli/domain/resource/command.py`
- a base command plugin in `wip/src/ontobdc/cli/plugin/command/base.py`
- pre-dispatch invocation from `wip/src/ontobdc/cli/__init__.py`

This design shift should therefore be recorded explicitly.

## Decision

OntoBDC adopts a plugin-based CLI pre-dispatch layer that runs before the legacy monolithic CLI dispatcher.

The CLI root entrypoint now supports the following architecture:

- raw CLI arguments are first normalized by `CliCommandRunAdapter`
- the adapter resolves an appropriate command plugin through `CommandLoader`
- the resolved plugin implements `CliCommandPort`
- the plugin returns a structured response object rather than rendering directly
- the CLI root entrypoint renders that response through a dedicated rendering step
- if no plugin command handles the input, the legacy CLI flow remains available as fallback

This decision introduces a new architectural layer, not a full replacement of the legacy dispatcher in a single step.

## Rationale

This decision exists to establish a cleaner command architecture for the CLI root while preserving compatibility with the existing command surface.

### First-Class Command Abstractions

The CLI root should be able to treat command-like behaviors as explicit objects rather than ad hoc inline branches.

That includes behaviors such as:

- root help
- root flags
- future CLI-level command handlers

### Extensibility

The project already uses plugin discovery successfully in other parts of the runtime.

Applying a similar pattern to the CLI makes it possible to:

- introduce new handlers incrementally
- reduce central dispatcher growth
- attach metadata to command handlers
- scope handlers by logical component

### Structured Responses

Commands should return structured response objects rather than coupling execution directly to one rendering method.

This enables:

- consistent rendering
- easier testing
- future support for multiple render modes
- clearer separation between command execution and response presentation

### Incremental Migration

The legacy dispatcher still carries most of the CLI behavior.

The pre-dispatch plugin layer provides a safe migration path:

- add one command handler at a time
- keep the old flow for everything else
- validate behavior incrementally

## Consequences

### Positive

- the CLI root gains a formal command abstraction
- command discovery becomes plugin-oriented rather than fully hardcoded
- root-level behaviors such as `--help` can be expressed as command plugins
- command execution and command rendering become more clearly separated
- structured responses provide a better base for future renderers and tests
- the migration can happen incrementally without rewriting the full CLI at once

### Negative

- the CLI now contains two dispatch models during the transition period
- plugin loading introduces additional runtime complexity
- partial or broken command plugins can interfere with discovery if the loader scans too broadly
- the current `CommandLoader` still has uneven maturity compared with capability and parameter loaders
- contributors must understand ports, adapters, loader behavior, and legacy fallback together

### Neutral

- the legacy `if` / `elif` dispatcher is not immediately removed
- command plugins currently coexist with the historical CLI implementation
- early response rendering may still be simple, including plain JSON-style output

## Alternatives Considered

### Keep All CLI Dispatch In `cli/__init__.py`

Rejected because the central dispatcher would continue to accumulate parsing, execution, and rendering responsibilities in one place.

### Replace The Legacy Dispatcher Immediately

Rejected because the current CLI surface is broad and operationally important.

A direct rewrite would raise migration risk and make it harder to validate behaviors incrementally.

### Add More Helper Functions But Keep No Command Plugin Layer

Rejected because helper extraction alone does not create:

- a discoverable command model
- plugin-oriented extensibility
- a stable response contract

### Use Plugins Only For Business Commands, Not For CLI Root Flags

Rejected because root CLI behaviors such as `--help` are precisely the kind of command-like behavior that benefits from first-class modeling in the new architecture.

## Implementation Notes

The current implementation reflects this decision through the following elements.

### Pre-Dispatch In The CLI Root

`wip/src/ontobdc/cli/__init__.py` now attempts to resolve and run a command plugin before entering the legacy CLI flow.

The current sequence is:

1. Build `incoming_args`.
2. Determine the render mode.
3. Resolve a command through `CliCommandRunAdapter.make(...)`.
4. If `check()` succeeds:
   - run the command
   - render the structured response
   - exit early
5. If command resolution raises `CliCommandArgumentException`, fall through to the legacy dispatcher.

### Command Request Model

`CliCommandRequest` in `wip/src/ontobdc/cli/adapter/command.py` normalizes the incoming request information passed to command plugins.

Its current shape includes:

- `logical_component`
- `component_action`
- `command_args`

### Command Port

`CliCommandPort` defines the minimum command contract:

- `check() -> bool`
- `run()`

The port also carries:

- `METADATA: CliCommandMetadata`

### Metadata Model

`CliCommandMetadata` introduces a metadata contract for CLI command plugins.

The current minimum fields are:

- `id`
- `logical_component`
- `description`

### Response Model

The CLI now has structured response dataclasses in:

- `wip/src/ontobdc/cli/domain/resource/command.py`

The current model includes:

- `CommandResponse`
- `HelpCommandResponse`

### Base CLI Command Plugin

`wip/src/ontobdc/cli/plugin/command/base.py` is the first concrete CLI command plugin in this architecture.

It currently acts as the handler for root help-like arguments:

- `--help`
- `-h`

It returns a `HelpCommandResponse` instead of printing directly from the command.

### Component Adoption

The architecture is actively expanding to other core components. For instance, the `storage` component now uses this plugin-based model for command handlers such as:

- `base`
- `enable`
- `list`
- `create`
- `delete`

These handlers return structured `CommandResponse` subclasses, while lower-level storage consistency logic remains in Python adapters and storage check/hotfix modules below the CLI command surface.

### Command Argument Exception

The CLI now includes a dedicated exception type:

- `CliCommandArgumentException`

This exception is used to signal that a command plugin could not accept the provided CLI arguments and that resolution should fall back safely.

## Transitional Notes

This decision is intentionally transitional.

The new architecture is active, but not yet fully generalized.

Known transitional properties include:

- the base CLI command plugin and the `storage` plugins are implemented, but a broader family of legacy CLI commands are still waiting to be migrated
- the `storage` component already combines plugin-dispatched commands with internal repository and integrity helpers, which shows the intended separation between CLI command surface and component internals
- `CommandLoader` still scans command plugins across components
- incomplete command plugins outside `cli` can still surface warnings during discovery
- the legacy dispatcher remains the operational fallback for most commands

This is acceptable under the current migration strategy.

## Risks And Constraints

The current design introduces several risks that must be acknowledged explicitly.

### Cross-Component Discovery Noise

Because command discovery is loader-based, incomplete command plugins in other components can produce warnings or empty discovery results during root CLI execution.

### Import Graph Sensitivity

The command loader and CLI adapter layers are sensitive to import ordering and circular dependencies while the architecture is still settling.

### Uneven Loader Contracts

The command loader is newer and less mature than the capability and parameter loaders.

This means contributors should treat command plugin discovery as an active architectural area rather than a fully stabilized contract.

## Future Direction

This ADR supports future work such as:

- introducing additional CLI command plugins beyond the base help handler
- narrowing command loader discovery by logical component
- improving loader diagnostics and failure visibility
- supporting richer render modes for `CommandResponse`
- progressively moving command-specific logic out of the legacy dispatcher
- eventually reducing or removing the monolithic `if` / `elif` command tree once plugin coverage becomes sufficient

## Related Documents

- [ADR003_plugin_oriented_capabilities_and_parameter_strategies.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/adr/ADR003_plugin_oriented_capabilities_and_parameter_strategies.md)
- [ADR007_shell_wrappers_as_stable_interface_and_python_as_primary_logic.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/adr/ADR007_shell_wrappers_as_stable_interface_and_python_as_primary_logic.md)
- [SPEC002_cli_help_from_pyproject_metadata.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC002_cli_help_from_pyproject_metadata.md)
- [SPEC010_shared_plugin_loaders.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC010_shared_plugin_loaders.md)
