# SPEC 006 - Run CLI Context Resolution

## Status

- **Status**: Working specification of the current `ontobdc run` CLI context model
- **Scope**: `wip/src/ontobdc/run/adapter/context.py` and the parameter strategies loaded into it
- **Audience**: maintainers and contributors working on CLI parsing, capability targeting, and runtime extensibility

## 1. Purpose

This specification describes how the `ontobdc run` context is built from CLI arguments before capability selection or execution happens.

The context layer exists to:

- normalize raw CLI arguments into structured parameters
- preserve unknown arguments for later inspection
- provide a repository root to downstream execution flows
- support both built-in and project-defined parameter strategies
- determine whether a capability has enough required inputs to be considered executable

This document focuses on the behavior currently exercised by:

- `test/src/ontobdc/run/adapter/test_context.py`
- `test/src/ontobdc/run/adapter/test_context_config.py`

## 2. Source Of Truth

This specification is derived from the current implementation under:

- `wip/src/ontobdc/run/adapter/context.py`
- `wip/src/ontobdc/shared/adapter/plugin.py`
- `wip/src/ontobdc/run/plugin/parameter/*.py`

The active automated tests covering this behavior are:

- `test/src/ontobdc/run/adapter/test_context.py`
- `test/src/ontobdc/run/adapter/test_context_config.py`

## 3. Runtime Role

The `run` context layer is the normalization boundary between:

- raw terminal input such as `argv`
- the capability execution layer

It does not execute a capability.

Its responsibility is to create a `CliContextPort` instance whose parameter map can later be used to:

- identify a targeted capability
- resolve repository location
- expose parsed filters and flags
- verify capability input satisfaction

In practice, this means the context layer is the parsing and enrichment stage of `ontobdc run`.

## 4. Core Model

### 4.1 `CliContextAdapter`

The current concrete context object is `CliContextAdapter`.

It stores:

- `raw_args`
  - the original `argv` sequence
- `unprocessed_args`
  - all arguments except `argv[0]`, progressively reduced as strategies consume known flags and values
- `parameters`
  - a dictionary keyed by logical parameter name, with values shaped as metadata dictionaries

### 4.2 Parameter Map Contract

Each parsed parameter is stored under a logical key such as:

- `capability_id`
- `export`
- `help`
- `repository`
- `limit`
- `start`
- `file_name`
- `file_type`
- `raw_text_path`
- `action_only`
- `include_action`

Each value is a dictionary and may contain:

- `value`
- `param_uri`
- `uri`
- any other strategy-defined metadata

The current implementation does not enforce a single rigid schema beyond using dictionaries.

### 4.3 Convenience Properties

The adapter currently exposes two derived properties:

- `target_capability_id`
  - returns `parameters["capability_id"]["value"]` when available
- `is_capability_targeted`
  - returns `True` when `target_capability_id` is not `None`

This means a malformed `--id` sequence may still create a `capability_id` entry while leaving the target unresolved.

## 5. Root Path Resolution

The context adapter also exposes `root_path`.

Current behavior:

- start from `os.getcwd()`
- walk upward until a `.__ontobdc__/config.yaml` file is found
- return that directory if found
- otherwise return the current working directory

This root discovery is used later by parameter strategies and by the resolver when looking for project-local context configuration.

The current tests validate both:

- explicit repository override via CLI flags
- fallback to current working directory when no repository flag is present

## 6. Resolution Pipeline

### 6.1 Resolver Entry

The runtime entrypoint for context building is `CliContextResolver.resolve(argv)`.

The current pipeline is:

1. Create a `CliContextAdapter(argv)`.
2. Load built-in parameter strategies using `ParameterLoader`.
3. Look for `.__ontobdc__/config.yaml` under `context.root_path`.
4. If present, load project-defined custom strategy packages from `capability.parameter`.
5. Append discovered custom strategies to the built-in strategy list.
6. Execute all strategies sequentially against the same mutable context.
7. Return the resulting context.

### 6.2 Ordering Semantics

The resolver is designed around strategy composition.

The current tests show that:

- supported parameters can appear in mixed order
- the final context is order-tolerant for the supported flag set

This does not mean all parameter combinations are commutative in an abstract sense.

It means the current built-in strategy set is robust to the tested permutations.

## 7. Built-In Strategy Model

Built-in strategies are discovered through `ParameterLoader`, which scans plugin packages under the current OntoBDC package tree.

The active built-in parameter strategy modules currently include:

- `action_only.py`
- `capability.py`
- `export.py`
- `file_filter.py`
- `help.py`
- `include_action.py`
- `pagination.py`
- `root_path.py`
- `text_file.py`

Each strategy:

- inspects `context.unprocessed_args`
- extracts the flags it recognizes
- writes normalized values into `context.parameters`
- removes consumed arguments from `context.unprocessed_args`

## 8. Current Built-In Parameters

The tests in `test_context.py` currently validate the following built-in behaviors.

### 8.1 Capability Targeting

Flag:

- `--id <value>`

Behavior:

- stores `capability_id`
- sets `target_capability_id`
- marks `is_capability_targeted` as `True`

If `--id` is missing a usable value:

- `capability_id` is still registered
- its `value` becomes `None`
- `is_capability_targeted` becomes `False`

### 8.2 Export Format

Flag:

- `--export <json|rich>`

Behavior:

- stores `export`
- only accepts `json` or `rich`

Failure behavior:

- raises `ValueError` for invalid formats
- raises `ValueError` for missing values

### 8.3 Help

Flags:

- `-h`
- `--help`

Behavior:

- stores `help=True`
- removes help flags from `unprocessed_args`

### 8.4 Repository Selection

Flags:

- `--root-path <path>`
- `--repository <path>`

Behavior:

- stores `repository` as a `LocalDirectoryRepository`
- `--root-path` has priority over `--repository`
- when neither flag is given, the repository defaults to the current working directory discovered by the adapter

### 8.5 Pagination

Flags:

- `--start <integer>`
- `--limit <integer>`

Behavior:

- stores `start` and `limit` as integers

Failure behavior:

- raises `ValueError` for invalid numeric values
- raises `ValueError` for missing values

### 8.6 File Filtering

Flags:

- `--file-name <pattern>`
- `--file-type <type[,type...]>`

Behavior:

- stores `file_name` as a string
- stores `file_type` as a list of strings

### 8.7 Raw Text File

Flag:

- `--text-file <path>`

Behavior:

- stores `raw_text_path`

### 8.8 Action Flags

Flags:

- `--action-only`
- `-a`

Behavior:

- `--action-only` stores `action_only=True`
- `-a` participates in include-action semantics and stores `include_action=True`

The include-action strategy also supports additional aliases such as `-auc`, `-uca`, and `--all`, even though those aliases are not exercised directly by the two adapter tests documented here.

## 9. Unknown Argument Preservation

One explicit contract of the resolver is preservation of unknown arguments.

If an argument is not recognized and consumed by any strategy:

- it remains in `context.unprocessed_args`

This is important because:

- the parser is intentionally strategy-driven rather than monolithic
- downstream layers can still inspect leftover arguments
- the system can distinguish between recognized parameters and unhandled input

The main mixed-parameter test currently verifies that after all known strategies run:

- only the truly unknown argument remains

## 10. Project-Defined Custom Strategies

### 10.1 Configuration Source

The resolver supports loading custom parameter strategies from:

- `.__ontobdc__/config.yaml`

The active configuration key is:

- `capability.parameter`

Expected shape:

```yaml
capability:
  parameter:
    - some.python.package
```

Each listed entry is expected to be a Python package, not just a single module file.

### 10.2 Discovery Model

For each configured package:

1. Import the package.
2. Ignore it if it is not package-like, meaning it has no `__path__`.
3. Walk submodules inside that package.
4. Import each submodule.
5. Instantiate every class that subclasses `CliContextStrategyPort`.
6. Append those strategy instances to the resolver pipeline.

### 10.3 Execution Model

Custom strategies execute in the same mutable context model used by built-in strategies.

That means a custom strategy may:

- inspect `unprocessed_args`
- add parameters
- remove consumed flags and values

The dedicated config test validates this with a temporary package providing a `CustomFlagStrategy` that parses:

- `--custom-flag <value>`

### 10.4 Legacy Keys

The resolver currently ignores legacy configuration keys such as:

- `parameters`
- `strategies`

Only `capability.parameter` is active in the current design.

## 11. Error Tolerance In Config Loading

The custom strategy loading layer is intentionally tolerant.

Current behavior:

- if `config.yaml` does not exist, continue with built-in strategies only
- if YAML is invalid, ignore the failure and continue
- if a configured package cannot be imported, ignore the failure and continue
- if a configured entry resolves to a non-package module, ignore it

This tolerance is validated directly by `test_context_config.py`.

The purpose of this behavior is runtime resilience:

- project-local extension must not break the base resolver entirely

## 12. Capability Satisfaction Contract

Beyond raw parsing, `CliContextResolver` also exposes `is_satisfied_by(capability, context)`.

Current behavior:

1. Read `capability.METADATA.input_schema.properties`.
2. Collect every property whose metadata contains `required: True`.
3. For each required property:
   - fail if the parameter key does not exist in the context
   - fail if the parameter exists but its `value` is `None`
4. Return `True` only when all required parameters are present with non-null values

This means context satisfaction is currently:

- metadata-driven
- based on logical parameter names
- strict for missing and null required values

## 13. Operational Implications

The current context model implies the following runtime design choices.

### 13.1 The Context Layer Is Extensible

New CLI parsing behavior does not require rewriting a central parser.

Instead, contributors can:

- add a new parameter strategy plugin
- or register a project-local custom strategy package through `config.yaml`

### 13.2 Parsing Is Partially Strict

Some invalid parameter states raise explicit exceptions, especially for:

- export format
- pagination values

Other states are tolerated and preserved, especially for:

- unknown flags
- missing config
- custom strategy loading failures

### 13.3 Repository Resolution Is Always Present

Even when no repository flag is supplied, the resolver still injects a repository object.

This makes downstream capability code simpler because a repository parameter is expected to exist after normal resolution.

## 14. Test Coverage Summary

### 14.1 Covered By `test_context.py`

- mixed built-in parameter parsing
- unknown argument preservation
- capability targeting state
- repository alias behavior
- repository default behavior
- missing capability value behavior
- invalid export handling
- missing export value handling
- invalid limit handling
- missing start value handling

### 14.2 Covered By `test_context_config.py`

- loading custom strategies from `capability.parameter`
- execution of a custom strategy against the context
- ignoring legacy config keys
- ignoring missing custom packages
- tolerating invalid YAML
- falling back to built-in strategies when config is absent
- ignoring non-package custom modules

## 15. Current Limitations

The current implementation has some notable limitations.

- Strategy ordering is implicit; there is no explicit priority model.
- Invalid custom strategy definitions are silently ignored.
- Error reporting for config-driven extension is intentionally minimal.
- The resolver mutates a shared context object rather than returning immutable snapshots.
- Satisfaction checks only inspect `required: True`; they do not validate types, enums, or richer schema rules.

## 16. Guidance For Contributors

When adding a new CLI parameter to `ontobdc run`, the current recommended path is:

1. Create a new strategy under `wip/src/ontobdc/run/plugin/parameter`.
2. Parse only the flags owned by that strategy.
3. Write a normalized logical parameter key into the context.
4. Remove consumed args from `unprocessed_args`.
5. Add focused tests:
   - a strategy-level test when appropriate
   - a resolver-level test when integration with the aggregate context matters

When adding a project-local extension, use:

```yaml
capability:
  parameter:
    - your.package.name
```

and ensure that package exports submodules containing classes that subclass `CliContextStrategyPort`.
