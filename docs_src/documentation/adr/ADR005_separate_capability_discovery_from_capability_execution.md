# ADR 005: Separate Capability Discovery From Capability Execution

## Status

Accepted

## Context

OntoBDC exposes at least two user-facing flows that operate over the same capability ecosystem:

- `ontobdc list`
- `ontobdc run`

Both commands depend on capability discovery and metadata, but they do not have the same responsibility.

At a product level, users need two different experiences:

- a read-only catalog view of what is available
- an execution flow that resolves parameters, targets a capability, validates required context, and runs it

If these concerns are collapsed into one command or one runtime layer, the system becomes harder to reason about.

In particular, a merged model would create recurring problems:

- discovery behavior could become coupled to execution side effects
- read-only inspection could accidentally inherit execution-time requirements
- execution logic could become polluted with presentation concerns meant only for catalog browsing
- future refactors might turn `list` into a thin alias of `run`, losing the distinction between “what exists” and “what can be executed now”

The current architecture already shows a deliberate separation.

The `list` component:

- discovers capabilities
- extracts and normalizes metadata
- renders a catalog in rich or JSON form
- does not execute capabilities
- does not evaluate capability satisfaction against CLI context

The `run` component:

- resolves CLI context
- loads parameter strategies
- targets a specific capability or supports selection behavior
- evaluates whether required parameters are satisfied
- executes the chosen capability
- renders execution results

This distinction is central enough to be treated as an architectural decision.

## Decision

OntoBDC separates capability discovery from capability execution.

This means:

- `ontobdc list` is the read-only discovery and catalog surface
- `ontobdc run` is the targeting, satisfaction, and execution surface

### `list`

The `list` component exists to expose the discoverable capability catalog.

Its role is to:

- load discoverable capabilities
- extract and normalize capability metadata
- present that metadata to the user

It must not:

- execute capabilities
- require capability targeting
- evaluate whether a capability is executable for the current CLI context
- mutate runtime state as part of normal listing behavior

### `run`

The `run` component exists to execute capabilities.

Its role is to:

- build a runtime context from CLI input
- resolve repository and parameter inputs
- determine which capability is targeted or selectable
- evaluate whether the chosen capability has the required context
- execute that capability
- render its result

It may reuse the same capability discovery layer used by `list`, but it must remain a distinct execution-oriented flow.

### Shared Capability Ecosystem

`list` and `run` are allowed to share:

- capability loaders
- metadata contracts
- plugin-oriented capability discovery

But they must not collapse into a single undifferentiated runtime path.

Shared discovery is acceptable.

Shared responsibility is not.

## Rationale

This decision exists to preserve four important properties of the system:

- conceptual clarity
- safe read-only inspection
- execution isolation
- future maintainability

### Conceptual Clarity

Users should be able to answer two different questions with two different commands:

- “What capabilities exist?”
- “Run this capability now.”

Keeping `list` and `run` distinct makes the CLI easier to understand and document.

### Safe Read-Only Inspection

Catalog browsing should not require execution intent.

A user should be able to inspect the capability space without entering the execution flow, satisfying capability inputs, or triggering operational side effects.

### Execution Isolation

Execution requires more than discovery.

It requires:

- context resolution
- parameter normalization
- satisfaction checks
- targeting or selection
- output rendering tied to execution

This logic belongs in `run`, not in the catalog flow.

### Future Maintainability

The separation reduces the risk that future changes to execution behavior will unintentionally degrade discovery behavior, or vice versa.

It also supports clearer tests, clearer specs, and clearer component ownership.

## Consequences

### Positive

- `list` remains a predictable read-only catalog view
- `run` remains focused on execution semantics
- documentation can describe discovery and execution as distinct use cases
- tests can validate catalog behavior separately from execution behavior
- shared discovery infrastructure can evolve without forcing `list` and `run` into the same command shape

### Negative

- some discovery logic is conceptually present in more than one component path
- contributors must understand the difference between metadata exposure and executable capability resolution
- there is pressure to keep the shared capability model aligned across both components

### Neutral

- this does not forbid shared loaders or shared metadata normalization helpers
- this does not require that `list` and `run` use completely different internals
- the separation is architectural and behavioral, not a requirement for total code duplication avoidance

## Alternatives Considered

### Merge `list` Into `run`

Rejected because it would blur the distinction between browsing capabilities and executing them.

It would also make read-only inspection more dependent on execution-oriented logic.

### Make `list` A Thin Alias Of `run --list`

Rejected because it would encourage the execution layer to absorb catalog responsibilities and would weaken the conceptual role of `list` as a dedicated discovery component.

### Hard Split With Completely Independent Discovery Stacks

Rejected because shared capability discovery infrastructure is useful and does not conflict with architectural separation as long as component responsibilities remain distinct.

## Implementation Notes

The current repository reflects this decision through:

- `wip/src/ontobdc/list`
  - read-only capability listing
- `wip/src/ontobdc/run`
  - runtime context resolution and execution
- shared discovery support through loader infrastructure

The current specifications that describe this distinction are:

- [SPEC004_component_flows.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC004_component_flows.md)
- [SPEC005_ontobdc_list_component.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC005_ontobdc_list_component.md)
- [SPEC006_run_cli_context_resolution.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC006_run_cli_context_resolution.md)

This ADR should also be read together with:

- [ADR003_plugin_oriented_capabilities_and_parameter_strategies.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/adr/ADR003_plugin_oriented_capabilities_and_parameter_strategies.md)

## Future Direction

This decision supports future work such as:

- expanding `list` as a richer catalog without contaminating it with execution semantics
- strengthening `run` satisfaction and targeting rules without turning catalog browsing into an execution preflight
- sharing capability metadata infrastructure while preserving separate command identities
- preventing regressions in which discovery and execution are re-merged into one ambiguous flow
