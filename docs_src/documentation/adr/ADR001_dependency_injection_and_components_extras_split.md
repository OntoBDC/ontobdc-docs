# ADR 001: Use Dependency Injection And Split The System Into Core Components And Optional Extras

## Status

Accepted

## Context

OntoBDC needs to support more than one functional area without turning the core into a monolithic package.

The project already contains multiple concerns with different operational and dependency profiles, including:

- core CLI routing and initialization
- infrastructure checks
- capability discovery and execution
- capability listing
- dataset storage management
- developer workflows
- A3-oriented flows
- optional semantic and social capabilities

These areas do not have the same runtime weight, maintenance cost, or installation requirements.

For example:

- the core CLI should remain usable with a smaller mandatory dependency surface
- storage features require additional packages
- A3 features require their own semantic validation stack
- future features may need to extend the system without becoming part of the minimal core installation

At the same time, the codebase already shows a structural preference for:

- ports
- adapters
- shared abstractions
- plugins
- domain-oriented modules

This implies an architectural direction in which feature logic should depend on abstractions and injected implementations, not on hardcoded concrete dependencies tied directly to a monolithic runtime.

## Decision

OntoBDC adopts dependency injection as a guiding architectural principle and organizes its functionality into:

- a **core** distribution
- distinct **components** inside the core runtime
- optional **extras** for capability areas with additional dependency requirements

### Dependency Injection

The system should prefer dependency flow through:

- ports
- adapters
- repositories
- strategy objects
- plugin discovery

instead of tightly coupling high-level flows directly to concrete implementations.

In practice, this means:

- domain logic should target interfaces or stable abstractions where possible
- adapters should provide environment-specific or infrastructure-specific behavior
- components should be replaceable or extensible without requiring a redesign of the entire CLI
- optional feature families should remain attachable without inflating the core package by default

### Components

The core runtime is organized into explicit functional components, such as:

- `cli`
- `check`
- `run`
- `list`
- `storage`
- `dev`
- `a3`
- `shared`
- `module`

These components are treated as conceptual and operational slices of the core system rather than as one undifferentiated command surface.

### Extras

Feature sets with additional dependency requirements must be represented as optional extras when appropriate.

The current packaging model already reflects this through extras such as:

- `storage`
- `dev`
- `a3`
- `a3-openai`
- `social`

These extras extend the core package without redefining the core itself.

## Rationale

This decision exists to preserve three things at the same time:

- a small and coherent core
- extensibility across domains
- architectural separation between contracts and implementations

Without this split, OntoBDC would tend toward:

- a heavier mandatory install
- stronger cross-component coupling
- more brittle command evolution
- higher difficulty when deprecating, moving, or externalizing features

With this split, the project can:

- keep the minimal runtime focused on the current core command surface
- add or remove optional capabilities with less disruption
- move legacy or specialized behavior out of the core more safely
- support future companion packages and extra-specific execution flows

## Consequences

### Positive

- the core package remains smaller and more focused
- optional capabilities can evolve with less pressure on the base installation
- components become easier to reason about, document, and test
- infrastructure-dependent behavior can live behind adapters and ports
- future deprecations and migrations become easier to manage

### Negative

- the architecture becomes more abstract and may feel heavier for small features
- contributors must understand the separation between component, adapter, domain, and extra
- packaging and documentation must stay aligned with the actual component and extra boundaries

### Neutral

- not every component necessarily maps one-to-one to a Python extra
- some components remain part of the core surface even when they use optional or gated behavior
- the split is architectural and packaging-oriented, not only directory-oriented

## Alternatives Considered

### Single Monolithic Core Package

Rejected because it would force unrelated dependency sets into the base installation and would make feature evolution harder.

### Feature Split Without Dependency Injection

Rejected because packaging separation alone would not solve the coupling problem inside the runtime design.

### Pure Plugin-Only Architecture With No Core Component Model

Rejected because the system still needs a stable, documented core command surface and a coherent runtime identity.

## Implementation Notes

The current repository reflects this decision through:

- component-oriented organization in `wip/src/ontobdc`
- ports and adapters in domain-specific areas
- plugin-oriented extension points
- optional dependency groups in `wip/pyproject.toml`
- command metadata that labels commands by component and source

This ADR should be read together with:

- [SPEC001_core_modules_and_commands.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC001_core_modules_and_commands.md)
- [SPEC005_cli_help_from_pyproject_metadata.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC005_cli_help_from_pyproject_metadata.md)

## Future Direction

This decision supports future moves such as:

- extracting specialized behavior into companion packages
- keeping legacy commands out of the active core surface
- unifying related command families without collapsing architectural boundaries
- expanding optional domain packages without redefining the base OntoBDC runtime
