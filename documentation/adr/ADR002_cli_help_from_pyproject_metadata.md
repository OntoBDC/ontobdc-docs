# ADR 002: Build CLI Help From `pyproject.toml` Metadata

## Status

Accepted

## Context

The OntoBDC CLI historically rendered its top-level help from hardcoded strings inside the Python entrypoint.

That approach caused a few recurring problems:

- the command catalog in the CLI could drift from the documented command surface
- command descriptions had to be updated in more than one place
- legacy or deprecated commands could remain exposed in help text longer than intended
- subcommand help behavior could evolve inconsistently across the CLI

At the same time, the project already started to consolidate command metadata in `pyproject.toml` under a custom `tool.ontobdc.commands.*` section.

This created an opportunity to make the help output derive from a single metadata source instead of keeping the displayed command catalog hardcoded in `src/ontobdc/cli/__init__.py`.

## Decision

The OntoBDC CLI help must be generated from metadata loaded through `ontobdc_data()`, which reads `pyproject.toml` and exposes its content as JSON-compatible data.

The top-level help now uses the `tool.ontobdc.commands` metadata as the source of truth for:

- command names
- command descriptions
- command usage-related information needed by the rendered help

This decision also applies to subcommand help flows when practical, starting with `ontobdc init -h` and `ontobdc init --help`, which now render through the standard `INFO` message box using metadata-derived content.

## Consequences

### Positive

- the command catalog has a single authoritative metadata source
- the CLI help becomes easier to keep aligned with product decisions
- removing or deprecating commands requires fewer code edits
- tests can validate help behavior against a stable metadata contract
- the standard `message_box.sh` presentation remains consistent across help flows

### Negative

- the CLI help now depends on the presence and correct structure of the custom `tool.ontobdc.commands` metadata
- malformed metadata can degrade help quality even if the runtime command still exists
- the project takes on responsibility for maintaining a custom metadata schema inside `pyproject.toml`

### Neutral

- this does not make the metadata a Python packaging standard; it remains a project-specific convention
- command visibility can still include runtime gating, such as optional exposure of `dev` and `a3`

## Alternatives Considered

### Keep help hardcoded in Python

Rejected because it duplicates information already being curated in `pyproject.toml` and increases drift risk.

### Generate documentation from code only

Rejected for now because the project already needs a stable human-editable metadata layer for command descriptions and usage examples.

### Store command metadata in a separate JSON or YAML file

Rejected for now because `pyproject.toml` already acts as the project metadata hub and is sufficient for this purpose.

## Implementation Notes

- `src/ontobdc/cli/__init__.py` loads command metadata through `ontobdc_data()`
- top-level help rendering no longer hardcodes the command catalog
- `src/ontobdc/cli/init.py` uses the same metadata source for `init` help
- dedicated tests validate help rendering and the use of the `INFO` message box contract

