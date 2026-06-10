# RFC 001 - Add Status Section To `ontobdc` CLI Help

## Status

- **Status**: requested
- **Scope**: top-level `ontobdc` help output
- **Primary surface**: `ontobdc`

## Purpose

This RFC proposes adding a `Status` section to the top-level `ontobdc` CLI help output before the current `Usage` section.

## Context

The current help output starts directly with `Usage`, then lists commands.

Today, it does not provide a quick health summary of the local project state.

That means the user still has to infer or separately inspect things such as:

- whether OntoBDC is initialized
- which engine is active
- whether a runtime context is active
- whether storage is initialized
- whether optional capabilities or modules are available

## Motivation

The top-level help command is often the first diagnostic surface a user sees.

Adding a `Status` block before `Usage` would make the CLI more operationally informative and reduce guesswork during normal use and troubleshooting.

## Proposal

Before the current `Usage` section, print a concise `Status` section summarizing the local project health.

Suggested placement:

1. `Status`
2. `Usage`
3. `Commands`

Suggested initial content:

- initialization state
- active engine
- runtime context presence
- storage index presence

Example sketch:

```text
Status:
  Initialized: yes
  Engine: venv
  Context: active
  Storage: available
```

## Constraints

The section should:

- stay concise
- avoid replacing `ontobdc check`
- avoid expensive runtime inspection
- remain safe to render even when the project is not initialized

## Expected Impact

If implemented, this change would affect:

- top-level CLI help rendering
- help-related shell tests
- command-surface documentation

Likely documentation updates:

- `docs/documentation/spec/SPEC001_core_modules_and_commands.md`
- `docs/documentation/spec/SPEC004_component_flows.md`
- `docs/documentation/test/TEST001_cli_component_tests.md`

## Open Questions

- Should `Status` be shown only for initialized projects, or always with graceful fallbacks?
- Should runtime context report only file presence, or also the evaluated machine state?
- Should the section include warning markers for degraded states?

## Follow-Up

If accepted, the next step should be to define the minimum stable health fields and their exact wording before changing the CLI output and tests.
