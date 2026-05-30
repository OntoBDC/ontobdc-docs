# OLD 004 - Legacy Note - CLI Help From `pyproject.toml` Metadata

## Purpose

This note summarizes the specification for building CLI help from `pyproject.toml` metadata.

## Removal Status

- **Status**: removed from the active documentation
- **Removed in version**: `0.9.0`

## Why It Was Removed

The project is no longer using `pyproject.toml` to document CLI commands.

## Historical SPEC Content

---

# SPEC 002 - CLI Help From `pyproject.toml` Metadata

## Status

- **Status**: Working specification of the current metadata-driven CLI help model
- **Scope**: `src/ontobdc/cli` and `pyproject.toml`
- **Audience**: maintainers and contributors of the OntoBDC core CLI

## 1. Purpose

This specification describes how the OntoBDC CLI help is built from metadata stored in `pyproject.toml` instead of being hardcoded directly in Python.

This document explains:

- what the metadata-driven help model is
- where the command metadata lives
- how the CLI reads and renders that metadata
- which fields are currently used
- how to add a new command to the metadata safely
- what metadata changes do not automatically make a command executable

## 2. Decision Context

The CLI help used to embed the command catalog directly in `src/ontobdc/cli/__init__.py`.

That created duplication between:

- runtime help text
- specs and ADRs
- product decisions about which commands are current, gated, deprecated, or legacy

The current model moves the command catalog into the custom `tool.ontobdc.commands.*` section of `pyproject.toml` and makes the CLI read it through `ontobdc_data()`.

The architectural rationale for this decision is recorded in [ADR002_cli_help_from_pyproject_metadata.md](docs/documentation/legacy/OLD003_cli_help_from_pyproject_metadata_adr.md).

## 3. Source Of Truth

The metadata source of truth is:

- `pyproject.toml`

The runtime readers are:

- `src/ontobdc/cli/__init__.py`
- `src/ontobdc/cli/init.py`

The primary metadata section is:

```toml
[tool.ontobdc.commands.<command_name>]
```

Examples currently present include:

- `cli`
- `init`
- `check`
- `run`
- `list`
- `storage`
- `dev`
- `a3`

## 4. Runtime Model

### 4.1 Metadata Loading

`ontobdc_data()` reads `pyproject.toml`, parses the TOML content, and exposes it as a JSON-compatible dictionary.

Its role is:

- locate `pyproject.toml`
- parse TOML
- normalize the result into JSON-safe Python data
- return `{}` on failure

This keeps the rest of the CLI logic independent from TOML parsing details.

### 4.2 Top-Level Help Rendering

`print_help()` reads:

- `tool.ontobdc.commands.cli`
- the command entries under `tool.ontobdc.commands.*`

It uses that metadata to build:

- the executable name used in the `Usage:` line
- the visible command catalog
- the short command descriptions shown in the help body

The top-level help is still rendered through the standard message box flow:

- color: `INFO`
- title type: `OntoBDC`
- title text: `CLI Help`

### 4.3 Subcommand Help Rendering

The same metadata model can also be used by subcommands.

The first implemented example is `ontobdc init -h` and `ontobdc init --help`, which now render through:

- color: `INFO`
- title type: `OntoBDC`
- title text: `Init Help`

using metadata read from:

- `tool.ontobdc.commands.init`

## 5. Metadata Schema

The metadata schema is project-specific and currently informal but stable enough for operational use.

The following fields are currently used or expected:

### 5.1 `component`

Functional ownership label for the command.

Example:

```toml
component = "core"
```

### 5.2 `source`

Internal source or implementation area associated with the command.

Example:

```toml
source = "cli.init"
```

### 5.3 `availability`

Human-readable visibility or gating note.

Examples:

```toml
availability = "always available"
availability = "requires initialized project"
availability = "requires initialized project and usually dev.tool enabled"
```

This field is descriptive, but some phrases are also used by the CLI as simple visibility gates in help rendering.

Current examples:

- commands mentioning `dev.tool enabled`
- commands mentioning `A3 enabled`

### 5.4 `usage`

List of usage examples for the command.

Example:

```toml
usage = [
    "ontobdc init <engine>",
    "ontobdc init",
    "ontobdc init -h | --help",
]
```

### 5.5 `description`

Single-line command description shown in help output.

Example:

```toml
description = "Initialize the local OntoBDC project configuration."
```

### 5.6 `options`

Human-readable list of options, arguments, or subcommand forms.

Example:

```toml
options = [
    "engine: explicit execution engine such as venv or colab",
]
```

### 5.7 `notes`

Optional explanatory list for additional behavioral context.

Example:

```toml
notes = [
    "If the engine is omitted, OntoBDC tries to auto-detect colab or an active virtual environment.",
]
```

## 6. How To Add A New Command

Adding a command to metadata is a documentation and help-surface step, not the full implementation step.

Use the following procedure.

### 6.1 Add The Metadata Entry

Create a new block in `pyproject.toml`:

```toml
[tool.ontobdc.commands.example]
component = "example"
source = "example"
availability = "requires initialized project"
usage = [
    "ontobdc example",
    "ontobdc example --help",
]
description = "Describe what the command does."
options = [
    "--help: show example help",
]
notes = [
    "Optional extra notes if needed.",
]
```

### 6.2 Keep The Entry User-Facing

Write the metadata as user-facing help text:

- short command names
- short descriptions
- readable examples
- readable option descriptions

Avoid implementation-only wording when the field is intended for the CLI help surface.

### 6.3 Wire The Runtime Command

Adding metadata alone does **not** make the command executable.

You must still:

- add routing in `src/ontobdc/cli/__init__.py`
- implement the command module or shell script
- decide whether the command is always available or gated
- add or update tests

If the runtime routing is missing, the help may show the command while execution still fails.

### 6.4 Add Command-Specific Help If Needed

If the command also has a dedicated subcommand help path, that implementation should read the same metadata instead of duplicating the content manually.

### 6.5 Add Tests

At minimum, consider:

- top-level help visibility
- subcommand `-h` / `--help`
- gating behavior when the command is conditional
- expected message box color/title contract

## 7. Current Limitations

The current implementation intentionally stays lightweight.

Known limitations include:

- the schema is not formally validated
- help rendering uses simple conventions rather than a strict metadata model
- some availability logic depends on matching phrases inside `availability`
- metadata can describe commands that are not yet fully wired
- malformed TOML or malformed command entries can degrade help quality

## 8. Practical Guidance

When changing command metadata:

- update `pyproject.toml` first
- verify top-level help output
- verify any dedicated subcommand help output
- verify the command still matches current product decisions
- remove deprecated commands from both metadata and routing when they leave the active surface

When deprecating a command:

- remove it from `tool.ontobdc.commands`
- remove or disable the CLI routing path
- update specs and tests
- record the reason in an ADR or legacy note when appropriate

## 9. Related Files

- [pyproject.toml](pyproject.toml)
- [__init__.py](src/ontobdc/cli/__init__.py)
- [init.py](src/ontobdc/cli/init.py)
- [ADR002_cli_help_from_pyproject_metadata.md](docs/documentation/legacy/OLD003_cli_help_from_pyproject_metadata_adr.md)
- [test_cli_help.sh](test/src/ontobdc/test_cli_help.sh)
- [test_cli_init_help.sh](test/src/ontobdc/test_cli_init_help.sh)
