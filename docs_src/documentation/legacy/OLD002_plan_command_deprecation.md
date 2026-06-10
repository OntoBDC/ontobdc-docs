# OLD 002 - Legacy Note - `ontobdc plan`

## Purpose

This note records the deprecation of the legacy `ontobdc plan` command and the reason it is no longer part of the active core CLI surface.

## Deprecation Status

- **Status**: deprecated and removed from the active core CLI surface
- **Deprecated in version**: `0.9.0`

## Why It Was Deprecated

`ontobdc plan` was deprecated because long-term planning behavior is intended to be unified into `ontobdc run` rather than maintained as a separate top-level command.

The direction is to keep execution, capability selection, and planning concerns converging in a single operational entrypoint instead of exposing a parallel planning-only command in the core CLI.

This future unification is expected to:

- reduce overlap between `run` and `plan`
- keep capability execution and execution planning in the same conceptual surface
- simplify the public command catalog
- reduce maintenance cost for duplicate argument parsing and command routing

## Historical Behavior

Before deprecation, `ontobdc plan` acted as a planning-oriented command that:

- loaded a target capability
- resolved dependencies and candidate providers
- built a dependency graph
- reported missing inputs, cycles, and possible execution order

## Historical Implementation Note

In the legacy core CLI, `ontobdc plan` was routed by a dedicated `plan_command()` path that delegated to `plan/plan.sh`.

That implementation is now treated as legacy behavior rather than part of the current supported command surface.
