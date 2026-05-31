# SPEC 005 - OntoBDC List Component

## Status

- **Status**: Working specification of the current `ontobdc list` component
- **Scope**: `wip/src/ontobdc/list` and its active CLI entrypoint behavior
- **Audience**: maintainers, contributors, and users of the OntoBDC core CLI

## 1. Purpose

This specification describes the current behavior of the `ontobdc list` component.

The component exists to expose the currently discoverable OntoBDC capabilities and their metadata without executing them.

This document focuses on:

- the command surface of `ontobdc list`
- how capability discovery currently works
- how output is rendered in rich and JSON modes
- how `list` relates to the shared capability catalog used by `run`
- current limitations and implementation notes

## 2. Source Of Truth

This specification is derived from the current implementation under:

- `wip/src/ontobdc/list/list.py`
- `wip/src/ontobdc/cli/__init__.py`
- `wip/src/ontobdc/shared/adapter/plugin.py`
- `wip/pyproject.toml`

The main automated test currently covering the component entrypoint is:

- `test/src/ontobdc/test_cli_list.sh`

## 3. Component Role

`ontobdc list` is the catalog view of the current capability ecosystem loaded by the core runtime.

Its role is to:

- discover available capabilities
- normalize their metadata into a serializable structure
- render that catalog either as JSON or as terminal-oriented rich cards

Unlike `ontobdc run`, this component does not execute a capability.

Its main responsibility is capability exposure, not capability resolution or execution.

## 4. Command Surface

According to the current command metadata:

- command: `ontobdc list`
- availability: requires initialized project
- source: `list`

The current command forms are:

- `ontobdc list`
- `ontobdc list --json`
- `ontobdc list --help`

The current metadata-defined options are:

- `--json`
  - output capability metadata as JSON
- `--help`, `-h`
  - show list help

## 5. Runtime Entry Behavior

The active runtime flow is split between the CLI entrypoint and the `list` module itself.

### 5.1 CLI-Level Gating

The top-level CLI currently enforces that `ontobdc list`:

- requires a valid initialized project
- is routed only after root and config resolution succeed

That means `list` is not available as a pre-init command in the normal CLI flow.

### 5.2 Help Routing

In the current runtime design, `ontobdc list --help` is intercepted by the main CLI entrypoint before `list.py` runs.

The effective help behavior therefore comes from:

- `wip/src/ontobdc/cli/__init__.py`
- metadata under `[tool.ontobdc.commands.list]` in `wip/pyproject.toml`

This means the effective user-facing help is metadata-driven and rendered through the standard CLI help contract.

`list.py` still contains an internal `show_help()` implementation, but that is no longer the primary runtime path when the command is invoked through the main `ontobdc` entrypoint.

## 6. Discovery Model

The component discovers capabilities through:

- `CapabilityLoader`

The loader scans plugin folders under the active OntoBDC package tree and loads capability classes that:

- are importable
- expose `METADATA`
- subclass the capability base contract

From the `list` component perspective, discovery is read-only.

It does not:

- mutate capability state
- execute a capability
- evaluate capability satisfaction against a CLI context

This makes `list` the broad catalog layer, while `run` is the filtered execution layer.

## 7. Metadata Extraction Model

For each discovered capability, the component currently extracts:

- `id`
- `version`
- `name`
- `description`
- `author`
- `tags`
- `supported_languages`
- `input_schema`
- `output_schema`
- `raises`
- `type`

The emitted `type` is currently normalized as:

- `capability`

### 7.1 Input Schema Normalization

The implementation performs limited normalization to improve serializability:

- when an input property contains a Python `type`, it is converted to `str(type)`
- when an input property contains a `check` list, each entry is stringified

This is intended to make JSON output safer and easier to consume.

### 7.2 Deduplication

After discovery, the component deduplicates the catalog by capability ID.

The current behavior is effectively:

- first collect discovered capability dictionaries
- then collapse them into a dictionary keyed by `id`
- finally render the deduplicated values

The practical effect is that the last collected entry for a repeated capability ID wins.

## 8. Output Modes

The component currently supports two output modes.

### 8.1 Rich Terminal Mode

Default invocation:

- `ontobdc list`

Behavior:

- renders a `Capabilities` header
- prints one rich panel per discovered capability
- includes key metadata such as:
  - id
  - version
  - description
  - inputs
  - outputs

This mode is oriented toward interactive inspection in the terminal.

### 8.2 JSON Mode

Invocation:

- `ontobdc list --json`

Behavior:

- emits a JSON array
- includes normalized capability metadata
- is suitable for machine consumption or downstream tooling

This mode is the machine-readable catalog representation of the component.

## 9. Unknown Arguments

The component parses known list-specific options and keeps unknown arguments separate.

When unknown arguments are present, the current implementation:

- does not fail immediately
- emits a warning message box
- ignores those arguments for the listing flow

This makes the current `list` behavior tolerant rather than strict.

## 10. Error And Empty-State Behavior

### 10.1 Empty Discovery

If no capabilities are discovered, the component emits a warning message box stating that no items were found.

### 10.2 Runtime Failure

If discovery or rendering raises an exception, the component emits:

- a red error message box
- title text: `Listing Failed`

and exits with a non-zero status.

## 11. Relationship To `run`

`list` and `run` share the same broader capability ecosystem but serve different responsibilities.

### 11.1 Shared Elements

Both rely on:

- capability discovery from the plugin loader
- capability metadata as a core contract

### 11.2 Different Responsibilities

`list`:

- catalogs all discoverable capabilities
- does not require capability targeting
- does not evaluate capability satisfaction against user parameters
- does not execute capabilities

`run`:

- resolves CLI context
- evaluates parameter-driven filtering and targeting
- may present interactive selection
- executes the final capability

In short:

- `list` is the catalog view
- `run` is the execution view

## 12. Current Test Coverage

The current dedicated CLI test for this component is:

- `test/src/ontobdc/test_cli_list.sh`

That test currently validates:

- `ontobdc list --help`
- the message-box contract of list help through the main CLI entrypoint
- rich output rendering
- JSON output rendering
- presence of a fake discovered capability used for test isolation

## 13. Limitations And Notes

The current implementation has a few important limitations or transitional characteristics.

### 13.1 Internal Help Is No Longer The Effective Help Path

`list.py` still contains an internal help renderer, but the active CLI entrypoint now intercepts help before `list.py` executes.

This means there is some implementation overlap between:

- the internal `show_help()` in `list.py`
- the active help path in `cli/__init__.py`

### 13.2 JSON Serialization Is Partially Normalized

The component normalizes some metadata fields for JSON output, but it does not define a formal exported schema version for the catalog payload.

### 13.3 Discovery Depends On Importable Plugin State

Capability discovery depends on the current importable package tree and runtime plugin loader behavior.

That means the visible catalog is a runtime-derived view, not a static registry.

## 14. Summary

`ontobdc list` is the current OntoBDC capability catalog component.

It:

- requires an initialized project
- discovers capabilities through the shared plugin loader
- emits either rich terminal output or JSON
- exposes capability metadata without execution
- complements `ontobdc run` by separating catalog visibility from execution flow

In the current architecture, `list` is the main read-only discovery surface of the OntoBDC core CLI.
