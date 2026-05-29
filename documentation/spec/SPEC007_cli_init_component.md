# SPEC 007 - OntoBDC Init Component

## Status

- **Status**: Working specification of the current `ontobdc init` component
- **Scope**: `src/ontobdc/cli/init.py`
- **Audience**: maintainers and contributors working on project bootstrap, CLI initialization, and local environment setup

## 1. Purpose

This specification describes the current behavior of the `ontobdc init` component implemented in `src/ontobdc/cli/init.py`.

The component exists to:

- initialize a local OntoBDC project
- create the base `.__ontobdc__` configuration directory
- persist the selected execution engine into `config.yaml`
- render command help and user feedback through the CLI presentation contract
- trigger an initial environment verification and repair flow after bootstrap

This document explains:

- the runtime role of `ontobdc init`
- the inputs and outputs of the component
- how engine detection and validation currently work
- how project configuration is written
- how the component integrates with shared CLI metadata and `check`
- current limitations and operational implications

## 2. Source Of Truth

This specification is derived from the current implementation under:

- `src/ontobdc/cli/init.py`
- `src/ontobdc/cli/__init__.py`
- `src/ontobdc/check/config.json`
- `pyproject.toml`

Related behavior is also influenced by:

- metadata loaded through `ontobdc_data()`
- shared CLI routing in `ontobdc.cli`
- shell helper scripts such as `message_box.sh` and `print_log.sh`

## 3. Component Role

`ontobdc init` is the bootstrap command of the current OntoBDC CLI.

Its responsibility is not to execute domain capabilities or inspect project data.

Its role is to establish the minimum local project state required by the rest of the CLI, including:

- a recognized project marker directory
- a persisted engine selection
- an absolute root path in the project config
- a follow-up environment check flow

In practice, this makes `init` the transition point between:

- a plain directory
- an initialized OntoBDC project directory

## 4. Command Surface

According to the current implementation and metadata-driven help model, the command supports:

- `ontobdc init <engine>`
- `ontobdc init`
- `ontobdc init -h`
- `ontobdc init --help`

The engine argument is currently positional and optional.

If the engine is omitted, the component attempts runtime auto-detection.

## 5. Runtime Entry Model

The public entrypoint in this module is:

- `init_main()`

Its current behavior is minimal:

- delegate directly to `init_engine_main()`

The effective initialization flow is therefore concentrated in:

- `init_engine_main()`

## 6. Functional Breakdown

The module currently contains five functional areas:

### 6.1 Dependency Extra Detection

`is_extra_enabled(extra_name)` checks whether all dependencies listed under a named extra in `pyproject.toml` are installed in the current environment.

It currently:

- locates `pyproject.toml`
- searches the target extra block with regex
- extracts quoted dependency strings
- strips version operators before lookup
- checks installation using `importlib.metadata.version`

Current characteristics:

- returns `False` if the file is missing
- returns `False` if parsing fails
- returns `False` if any dependency is missing
- returns `False` if no dependencies are found
- returns `True` only when all dependencies are present

This function is a general CLI utility but is not part of the active `init` execution path today.

### 6.2 Logging Wrapper

`log(level, message, *args)` is a presentation adapter around `print_log.sh`.

Its behavior is:

- locate the shell script relative to `init.py`
- invoke it through `subprocess.run(..., check=False)` if present
- fall back to `print()` when the script is unavailable

This keeps the module compatible with both richer shell-driven CLI output and simpler fallback execution environments.

### 6.3 Message Box Wrapper

`message_box(color, title_type, title_text, message)` is a presentation adapter around `message_box.sh`.

Its behavior is:

- locate the shell script relative to `init.py`
- invoke it through `subprocess.run(..., check=False)` if present
- fall back to `print()` when the script is unavailable

This is the main user-facing output channel for:

- help
- warnings
- initialization state feedback

### 6.4 Metadata-Driven Help Construction

`init_help_message()` builds the help message for `ontobdc init`.

It tries to load command metadata from:

- `tool.ontobdc.commands.init` in `pyproject.toml`

through:

- `ontobdc_data()`

If metadata loading fails, it falls back to hardcoded defaults.

The help payload currently includes:

- usage entries
- a description
- options
- notes

The function returns a formatted string containing ANSI styling, which is then passed to `message_box()` when help is requested.

### 6.5 Initialization Orchestration

`init_engine_main()` is the core orchestration function of the component.

It is responsible for:

- parsing `sys.argv`
- rendering help when requested
- resolving the target engine
- validating the engine against `check/config.json`
- creating `.__ontobdc__`
- writing `config.yaml`
- triggering `check_main(repair=True)`

## 7. Initialization Flow

The current initialization flow is:

1. Inspect `sys.argv[2:]` for `-h` or `--help`.
2. If help is requested, render a message box with `init_help_message()` and return.
3. Parse the optional positional `engine` with `argparse`.
4. If no engine is provided, try to auto-detect one.
5. Validate the resolved engine against `src/ontobdc/check/config.json` if that file exists.
6. Resolve the current working directory as the project root to initialize.
7. Build:
   - `.__ontobdc__/`
   - `.__ontobdc__/config.yaml`
8. If `config.yaml` already exists, emit a warning and stop.
9. Create the marker directory if needed.
10. Build the configuration payload.
11. Write the YAML file.
12. Invoke `check_main()` with a lightweight object whose `repair` attribute is `True`.
13. Swallow `SystemExit` from the check phase so that initialization is not treated as a full failure.

## 8. Engine Resolution Model

### 8.1 Explicit Engine

When the user provides a positional engine value, that value is used directly.

Example:

- `ontobdc init venv`

### 8.2 Auto-Detection

If the engine is omitted, the component performs automatic detection.

Current detection order:

1. If `/content` exists, choose `colab`
2. Else if `sys.prefix != sys.base_prefix`, choose `venv`
3. Else fail and request an explicit engine

This means the current implementation assumes:

- Google Colab environments expose `/content`
- active virtual environments can be detected through Python prefix divergence

### 8.3 Validation Against `check/config.json`

After resolution, the engine may be validated against:

- `src/ontobdc/check/config.json`

Current validation behavior:

- if the file is missing, validation is effectively skipped
- if the file exists but cannot be parsed, a warning is logged
- if a `config.engine` list is found, the resolved engine must be in that list
- otherwise the command exits with an error

## 9. Configuration Persistence Model

### 9.1 Target Location

The initialized project structure is currently:

```text
<cwd>/
  .__ontobdc__/
    config.yaml
```

The current working directory at invocation time is treated as the project root.

### 9.2 Minimum Persisted Data

The YAML payload currently includes at least:

```yaml
engine: venv
directory:
  root:
    absolute_path: /absolute/project/path
```

The exact engine value varies with explicit input or auto-detection.

### 9.3 File Creation Semantics

Current behavior:

- create `.__ontobdc__` if it does not exist
- stop early if `config.yaml` already exists
- write YAML using `yaml.dump(..., default_flow_style=False)`

Although the code contains a branch that reads an existing config file into `config_data`, that branch is currently unreachable in normal execution because the function returns early when `config.yaml` already exists.

## 10. Output Contract

The component currently emits output through a mix of:

- `message_box()`
- `log()`
- plain `print()`
- `sys.exit()`

### 10.1 Help Output

Help is rendered through:

- color: `INFO`
- title type: `OntoBDC`
- title text: `Init Help`

### 10.2 Already Initialized Output

If the project already has `.__ontobdc__/config.yaml`, the component emits:

- color: `YELLOW`
- title type: `Warning`
- title text: `Already Initialized`

and returns without modifying the existing configuration.

### 10.3 Error Output

Errors may be surfaced through:

- `log("ERROR", ...)`
- plain `print()`
- `sys.exit(1)`

The exact presentation depends on which branch fails and whether helper shell scripts are available.

## 11. Post-Initialization Check Integration

After writing `config.yaml`, the component imports and executes:

- `check_main`

It constructs a local lightweight argument object:

```python
class CheckArgs:
    repair = True
```

and invokes:

- `check_main(CheckArgs(), cwd)`

This implies the `init` component expects `check_main` to accept:

- an object exposing a `repair` attribute
- a project root path argument

If `check_main` exits the process through `SystemExit`, `init_engine_main()` catches it and suppresses it.

This means:

- initialization success is primarily tied to config creation
- post-init repair is treated as best-effort follow-up work

## 12. State Transitions

The component currently models three practical states.

### 12.1 Uninitialized Directory

Characteristics:

- no `.__ontobdc__/config.yaml`

Behavior:

- create the directory structure
- write config
- run check

### 12.2 Already Initialized Directory

Characteristics:

- `.__ontobdc__/config.yaml` already exists

Behavior:

- show warning
- do not rewrite config
- do not rerun initialization persistence

### 12.3 Invalid Initialization Attempt

Examples:

- engine could not be auto-detected
- engine is not in the allowed engine list
- YAML file cannot be written

Behavior:

- emit error-oriented output
- exit non-zero

## 13. Dependencies And Collaborators

The module depends on:

- Python standard library
  - `os`
  - `re`
  - `sys`
  - `argparse`
  - `json`
  - `subprocess`
- third-party package
  - `yaml`
- packaging metadata APIs
  - `importlib.metadata.version`
  - `importlib.metadata.PackageNotFoundError`

It collaborates with:

- `ontobdc.cli.ontobdc_data`
- `ontobdc.cli.check_main`
- `src/ontobdc/check/config.json`
- `pyproject.toml`
- `message_box.sh`
- `print_log.sh`

## 14. Architectural Characteristics

The current component is operationally effective but architecturally mixed.

It currently combines:

- CLI parsing
- metadata-driven help rendering
- environment detection
- configuration persistence
- subprocess-backed presentation
- post-bootstrap orchestration

This means the module behaves as a full command adapter and application service at the same time.

## 15. Current Limitations

The current implementation has several important limitations.

### 15.1 Mixed Responsibilities

The module combines presentation, parsing, persistence, validation, and orchestration in one file.

### 15.2 Strong `sys.argv` Coupling

The logic reads `sys.argv[2:]` directly, making reuse outside the main CLI entrypoint harder.

### 15.3 Limited Auto-Detection Model

Engine detection only recognizes:

- `colab`
- an already active virtual environment

It does not inspect project configuration, local tooling preferences, or other execution contexts.

### 15.4 Non-Idempotent Initialization

If `config.yaml` already exists, the command returns early instead of validating or reconciling the existing configuration.

### 15.5 Unreachable Update Branch

The code includes logic intended to read and update an existing config file, but that branch is effectively bypassed because the command returns before reaching it.

### 15.6 Best-Effort Post-Init Check

The post-init check is not treated as a strict part of initialization success because `SystemExit` is swallowed.

## 16. Operational Guidance

When modifying `ontobdc init`, contributors should preserve the following behavioral contracts unless intentionally changing them:

- help should remain metadata-driven when possible
- the initialized project root should be the current working directory
- the config file should store an absolute root path
- engine validation should remain consistent with `check/config.json`
- bootstrap should still work when shell helper scripts are missing

When refactoring this component, the most natural separation points are:

- help rendering
- engine resolution
- config repository or config writer logic
- post-init check orchestration
- CLI argument parsing

## 17. Related Specifications

- `docs/documentation/spec/SPEC002_cli_help_from_pyproject_metadata.md`
- `docs/documentation/spec/SPEC003_system_artifacts_by_component.md`
- `docs/documentation/spec/SPEC004_component_flows.md`
- `docs/documentation/spec/SPEC006_run_cli_context_resolution.md`
