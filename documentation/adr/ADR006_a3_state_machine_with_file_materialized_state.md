# ADR 006: Model A3 As A State-Machine Workflow With File-Materialized State

## Status

Accepted

## Context

The A3 module is not a simple one-shot command.

It represents a multi-stage lifecycle in which a source is:

- ingested
- normalized
- parsed
- translated
- validated
- reasoned
- dispatched

Each of these stages may succeed, fail, or be resumed later.

This creates an architectural problem:

- where should the current state of an A3 package live?

There are multiple possible models:

- keep state only in memory while a single process runs
- persist state in a database or separate metadata registry
- derive state from the presence of physical artifacts on disk

The current OntoBDC A3 implementation already follows the third model.

In practice, the lifecycle package itself is the state carrier.

Files such as:

- `raw.txt`
- `sanitized.txt`
- `parsed.json`
- `graph.ttl`
- `validated.txt`
- `reasoned.ttl`
- `event.jsonld`
- `err.json`

are not just outputs.

They are also state indicators.

At the same time, the transition logic is not ad hoc.

It is coordinated through a state-machine-oriented runtime in which workers:

- evaluate the current package state
- initialize the A3 state machine at that physical state
- execute valid transitions
- write the next artifact to disk

This is a central architectural decision and should be recorded explicitly.

## Decision

OntoBDC models A3 as a state-machine workflow whose runtime state is materialized by files in the lifecycle package directory.

This means:

- the authoritative state of an A3 package is derived from artifacts on disk
- transitions are coordinated by a state-machine-oriented execution flow
- each successful stage persists a concrete artifact representing the new state
- processing can resume from the most advanced recognized artifact already present

### File-Materialized State

The A3 lifecycle state is not primarily stored in:

- an in-memory session object
- a database row
- a separate state registry detached from package contents

Instead, the physical package contents are the operational state source.

The most advanced recognized artifact determines the current package state.

### State-Machine Coordination

The lifecycle is advanced through a state-machine-oriented flow rather than through a loose chain of shell steps.

Workers:

1. inspect package artifacts
2. derive the current lifecycle state
3. initialize the state machine at that state
4. execute the next valid transition
5. persist the output artifact of the destination state
6. reevaluate the package based on the new physical artifacts

This loop continues until the package reaches:

- a final successful state
- or an error state / failure interruption

### Package Directory As Execution Boundary

The A3 package directory is the unit of:

- state
- resume behavior
- artifact persistence
- failure diagnosis

This means an A3 package is both:

- the working data container
- the lifecycle state boundary

## Rationale

This decision exists to preserve four important properties of the A3 architecture:

- resumability
- inspectability
- deterministic stage boundaries
- operational robustness

### Resumability

Because state is derived from persisted artifacts, the A3 workflow can resume after interruption.

The system does not need a long-lived in-memory process to know where to continue.

If a package already contains `parsed.json`, the workflow can resume from the parsed state rather than restarting from raw ingestion.

### Inspectability

A package can be inspected directly by a user or maintainer without querying an external state store.

This makes debugging simpler because:

- artifacts are visible on disk
- intermediate outputs can be examined directly
- failure evidence can be retained alongside the package

### Deterministic Stage Boundaries

Each state transition corresponds to a concrete persisted artifact.

This creates a strong boundary between stages:

- one stage produces a known file
- the next stage consumes known files
- the worker can determine state from package contents

This is clearer than a design in which state changes happen only in memory and outputs are treated as secondary side effects.

### Operational Robustness

The file-materialized model reduces dependence on auxiliary infrastructure such as:

- databases
- external job coordinators
- global mutable state services

This keeps the A3 workflow closer to the repository- and artifact-oriented design already present in OntoBDC.

## Consequences

### Positive

- A3 processing is resumable from disk state
- package state is human-inspectable
- intermediate artifacts are preserved as part of the lifecycle trace
- transition failures can leave useful evidence such as `err.json`
- workers can operate independently on package directories
- the architecture fits naturally with OntoBDC's file-oriented and package-oriented design

### Negative

- stale or manually modified artifacts can affect the perceived state of a package
- state evaluation logic must stay aligned with the artifact contract
- the system must carefully define which file wins when multiple stage artifacts coexist
- file presence becomes part of the control plane, so accidental filesystem changes can alter execution behavior

### Neutral

- lifecycle artifacts are both outputs and state markers
- this model does not prevent additional metadata in the future, but such metadata must not replace the artifact-based state contract without an explicit architectural change
- the state machine and the artifact model are complementary parts of the same design, not competing mechanisms

## Alternatives Considered

### In-Memory Pipeline State Only

Rejected because it would make interruption recovery much harder and would lose the package-oriented trace of intermediate work.

### Database-Backed State Registry

Rejected because it would add operational complexity and weaken the direct relationship between package contents and lifecycle state.

### File Outputs With No Explicit State Machine

Rejected because the A3 lifecycle needs governed transitions, not just a loose sequence of independently invoked scripts.

The state-machine layer gives the workflow explicit transition semantics and guards.

## Implementation Notes

The current repository reflects this decision through:

- A3 lifecycle artifacts such as:
  - `raw.txt`
  - `sanitized.txt`
  - `parsed.json`
  - `graph.ttl`
  - `validated.txt`
  - `reasoned.ttl`
  - `event.jsonld`
  - `err.json`
- the A3 lifecycle/state machine implementation under `wip/src/ontobdc/a3/domain/machine`
- worker-oriented processing under the A3 execution flow
- state evaluation based on artifact presence

The specifications that currently describe this architecture are:

- [SPEC003_system_artifacts_by_component.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC003_system_artifacts_by_component.md)
- [SPEC004_component_flows.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC004_component_flows.md)

This ADR should also be read together with:

- [ADR001_dependency_injection_and_components_extras_split.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/adr/ADR001_dependency_injection_and_components_extras_split.md)

## Future Direction

This decision supports future work such as:

- refining the artifact precedence rules used to derive current state
- adding stronger diagnostics for inconsistent package contents
- expanding transition guards and validation without abandoning the file-materialized state model
- introducing complementary metadata only if it remains subordinate to the artifact-based lifecycle contract
