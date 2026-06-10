# ADR 003: Adopt A Plugin-Oriented Architecture For Capabilities And Run Parameter Strategies

## Status

Accepted

## Context

OntoBDC needs to support an execution model in which:

- capabilities can be discovered dynamically instead of being registered in a fixed command catalog
- CLI argument handling for `ontobdc run` can evolve without concentrating all parsing logic in one monolithic parser
- different domains can add new execution behaviors and new input interpretation rules without rewriting the core runtime

The current `run` flow already depends on more than one kind of extensibility.

At runtime, the system must be able to:

- discover executable capabilities from the OntoBDC package tree
- discover parameter strategies that interpret CLI flags and map them into context parameters
- optionally extend that parameter strategy set through project-local configuration
- keep capability discovery separate from capability execution
- keep parameter parsing separate from command routing

If these concerns were hardcoded into one central parser or one static registry, the system would become harder to evolve.

In particular, a monolithic design would create recurring problems:

- every new parameter would require editing a central parser block
- every new capability family would pressure the core to maintain hardcoded catalogs
- domain packages would be harder to add without touching the runtime entrypoint
- testing would become more coupled because parsing, discovery, and execution would be mixed together

The current codebase already points in a different direction through:

- `CapabilityLoader`
- `ParameterLoader`
- context strategies under `run/plugin/parameter`
- runtime context normalization in `run/adapter/context.py`
- project-local custom strategy loading via `.__ontobdc__/config.yaml`

This establishes a clear architectural pattern that deserves formal registration.

## Decision

OntoBDC adopts a plugin-oriented architecture for:

- capability discovery
- `ontobdc run` parameter parsing and context enrichment

This means the core runtime must prefer:

- loader-based discovery of capabilities
- loader-based discovery of parameter strategies
- strategy objects that consume known CLI inputs and enrich a shared context
- extension through packages and plugin modules rather than through hardcoded command-specific parsing logic

### Capabilities

Executable capabilities are not treated as a hardcoded list inside the `run` command.

Instead, the runtime discovers them dynamically through capability loaders that scan the active OntoBDC package tree for importable capability classes with valid metadata.

This means:

- capability exposure is plugin-oriented
- capability availability is runtime-derived
- new capability families can enter the system by becoming discoverable in the expected plugin structure

### Parameter Strategies

The `run` CLI does not use a single monolithic parser that owns every possible flag and input mapping.

Instead, it resolves a mutable CLI context and applies a sequence of parameter strategies that:

- inspect unprocessed arguments
- recognize the flags they own
- write normalized parameters into the context
- remove consumed arguments from the unprocessed set

This means each strategy owns a narrow parsing responsibility rather than participating in one large parser implementation.

### Project-Local Extension

The parameter strategy set may also be extended by project-local configuration through:

- `.__ontobdc__/config.yaml`
- `capability.parameter`

Configured custom strategy packages are discovered and appended to the built-in strategy pipeline when they are importable and structurally valid.

This extension model is intentionally tolerant:

- missing config does not break the resolver
- invalid or missing custom packages do not break the base runtime

## Rationale

This decision exists to preserve four properties of the `run` architecture:

- extensibility
- isolation of concerns
- incremental evolution
- testability

### Extensibility

New capabilities and new context parameters should be addable without redesigning the core command entrypoint.

By discovering capabilities and strategies through loaders, the system can grow by composition instead of by central branching logic.

### Isolation Of Concerns

The following concerns remain distinct:

- top-level CLI routing
- context building
- capability discovery
- capability selection
- capability execution

This separation is important because `run` is not just a command parser.

It is an execution broker that needs independently evolvable discovery and parsing layers.

### Incremental Evolution

As OntoBDC evolves, some parameters may remain core while others become domain-specific.

A strategy-oriented parser allows the system to:

- add new parameters with focused implementations
- remove or deprecate old parameters with localized change
- keep the runtime adaptable to new domains and package families

### Testability

A plugin-oriented and strategy-oriented design supports multiple testing layers:

- focused tests per strategy
- aggregate tests for the full context resolver
- separate tests for capability discovery
- separate tests for command entrypoints

This is harder to maintain in a design where parsing and execution are tightly coupled in one block.

## Consequences

### Positive

- capabilities are not tied to a hardcoded runtime catalog
- new CLI parameter behaviors can be added through focused strategies
- parsing responsibilities stay small and easier to test
- the `run` context remains an explicit intermediate artifact between CLI input and execution
- domain extensions can enter the system with less pressure on the core command router
- project-local custom strategies can extend parsing behavior without patching the runtime itself

### Negative

- runtime behavior becomes more implicit because discovery depends on loader rules and importable modules
- debugging missing capabilities or missing strategies can be less obvious than in a static registry
- strategy ordering is a real concern and is currently implicit rather than explicitly prioritized
- contributors must understand loaders, plugin structure, and context contracts to extend the runtime safely

### Neutral

- plugin-oriented does not mean unrestricted or ungoverned discovery; the runtime still depends on expected package structure and metadata contracts
- not every CLI command needs to use this architecture; this ADR is primarily about the `run` execution model and the supporting discovery layer

## Alternatives Considered

### Monolithic Parser Inside `run`

Rejected because it would centralize all current and future `run` parameters in one parser implementation, increasing coupling and reducing extensibility.

### Hardcoded Capability Registry

Rejected because it would make capability growth depend on manual central registration and would work against the package-oriented design already present in OntoBDC.

### Fully Static Runtime With No Project-Local Extension

Rejected because the system benefits from allowing controlled local extension of parameter strategies through configuration, especially in domain-specific or experimental contexts.

## Implementation Notes

The current repository reflects this decision through:

- `wip/src/ontobdc/shared/adapter/plugin.py`
  - `CapabilityLoader`
  - `ParameterLoader`
- `wip/src/ontobdc/run/adapter/context.py`
  - `CliContextAdapter`
  - `CliContextResolver`
- `wip/src/ontobdc/run/plugin/parameter/*.py`
  - built-in parameter strategies
- `.__ontobdc__/config.yaml`
  - `capability.parameter` for custom strategy packages

This ADR should be read together with:

- [SPEC001_core_modules_and_commands.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC001_core_modules_and_commands.md)
- [SPEC006_run_cli_context_resolution.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC006_run_cli_context_resolution.md)

## Future Direction

This decision supports future work such as:

- expanding domain-specific capability packages without hardcoding them into `run`
- formalizing strategy ordering rules when needed
- adding richer capability filtering while preserving the current context pipeline
- evolving the project-local extension model without collapsing discovery back into a monolithic parser
