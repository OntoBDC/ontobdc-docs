# ADR 004: Allow Project-Local Runtime Extension Through `.__ontobdc__/config.yaml`

## Status

Accepted

## Context

OntoBDC already supports a plugin-oriented runtime for capability discovery and CLI context strategies.

That architecture solves the problem of keeping the core extensible at the package level, but it does not fully answer a second question:

- how can an individual project extend the `run` context behavior without patching the core package or publishing a new global distribution?

Some extensions are not meant to become immediately part of the core runtime.

Examples include:

- project-specific parameter strategies
- local experiments for domain-specific flags
- temporary or transitional parsing behavior needed by one project
- package-local conventions that should not be hardcoded in the OntoBDC base runtime

If every such extension required editing the core package, the system would become slower to adapt and more tightly coupled to local project needs.

At the same time, unconstrained extension would create its own problems:

- local configuration could break the entire `run` command
- invalid packages could make the runtime fragile
- legacy keys could linger indefinitely without a clear active contract

The current implementation already resolves this tension with a concrete model:

- the project-local config file `.__ontobdc__/config.yaml`
- the active extension key `capability.parameter`
- tolerant loading of custom strategy packages

This behavior is now important enough to be treated as an architectural decision rather than as an incidental implementation detail.

## Decision

OntoBDC accepts project-local runtime extension of `run` context behavior through:

- `.__ontobdc__/config.yaml`
- the key `capability.parameter`

This mechanism is used to register additional custom parameter strategy packages that are appended to the built-in `CliContextResolver` strategy pipeline.

### Active Contract

The active configuration contract is:

```yaml
capability:
  parameter:
    - some.python.package
```

Each listed entry is expected to identify a Python package that contains one or more submodules defining classes that subclass `CliContextStrategyPort`.

### Runtime Behavior

When `CliContextResolver` resolves a context, it must:

1. load the built-in parameter strategies
2. look for `.__ontobdc__/config.yaml` under the resolved project root
3. read `capability.parameter` when present
4. import each configured package when possible
5. walk submodules inside those packages
6. instantiate valid custom strategy classes
7. append those strategies to the runtime pipeline

### Tolerance Rules

The extension layer is intentionally tolerant.

The runtime must continue to work when:

- the config file does not exist
- the YAML is invalid
- a configured package cannot be imported
- a configured entry resolves to a module that is not a package

In those cases, the system must fall back to built-in strategies instead of failing the full resolver.

### Legacy Keys

Legacy config keys such as:

- `parameters`
- `strategies`

are not part of the active extension contract and must not be treated as supported extension inputs.

## Rationale

This decision exists to preserve three goals simultaneously:

- project-level extensibility
- runtime resilience
- a clear boundary between core and local customization

### Project-Level Extensibility

Projects need a supported way to customize the `run` context model without forking the core.

Allowing project-local strategy packages gives each project a controlled extension point that remains consistent with the plugin-oriented architecture of the runtime.

### Runtime Resilience

Configuration-based extension is useful only if it does not make the base runtime brittle.

The decision to tolerate invalid YAML, missing packages, and non-package modules ensures that local experimentation does not destroy the normal operation of `run`.

### Core Versus Local Boundary

Not every useful parameter strategy belongs in the core package.

This ADR formalizes a boundary:

- core strategies live in the built-in plugin tree
- project-specific strategies may be registered locally through config

This lets the core remain general while still allowing local specialization.

## Consequences

### Positive

- projects can extend `run` without patching the OntoBDC core package
- experimental or domain-specific strategies can be adopted incrementally
- the built-in runtime remains the fallback even when local extension is misconfigured
- the extension model remains consistent with the broader strategy-oriented context architecture
- local runtime behavior can be customized using a file already owned by the project bootstrap model

### Negative

- part of the runtime behavior may now depend on project-local configuration that is not visible from the CLI surface alone
- debugging parsing behavior can become harder when custom strategies are present
- silent tolerance means some extension failures may go unnoticed without careful inspection
- local projects may diverge in context behavior if they rely heavily on custom strategy packages

### Neutral

- this mechanism extends the runtime at the project level, not the global package level
- this ADR does not require every project to use local custom strategies
- the extension point is scoped to context strategy loading, not to arbitrary command replacement

## Alternatives Considered

### No Project-Local Extension

Rejected because it would force all useful strategy evolution either into the core package or into ad hoc local patches.

### Strict Failure On Invalid Local Extension

Rejected because one broken project-local package or one malformed YAML file would make the entire `run` resolver fragile.

### Arbitrary Python Module Paths Without Package Structure

Rejected because package-oriented discovery is more consistent with the existing loader model and produces a clearer contract for extension authors.

## Implementation Notes

The current repository reflects this decision through:

- `wip/src/ontobdc/run/adapter/context.py`
  - `CliContextResolver.resolve()`
- `.__ontobdc__/config.yaml`
  - `capability.parameter`
- tests:
  - `test/src/ontobdc/run/adapter/test_context_config.py`

The dedicated test coverage currently validates:

- loading a custom strategy package from `capability.parameter`
- successful execution of the custom strategy
- ignoring legacy keys
- ignoring missing packages
- tolerating invalid YAML
- ignoring configured modules that are not packages

This ADR should be read together with:

- [ADR003_plugin_oriented_capabilities_and_parameter_strategies.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/adr/ADR003_plugin_oriented_capabilities_and_parameter_strategies.md)
- [SPEC006_run_cli_context_resolution.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC006_run_cli_context_resolution.md)

## Future Direction

This decision supports future work such as:

- documenting a more formal schema for project-local custom strategies
- adding better diagnostics for ignored or invalid custom packages
- defining explicit ordering or precedence rules between built-in and local strategies when needed
- deciding which successful local extensions should later be promoted into the core runtime
