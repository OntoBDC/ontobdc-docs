# RFC 004 - Hybrid LLM Layer As A Strict Normalization Interface

## Status

- **Status**: requested
- **Scope**: optional preprocessing interface before deterministic runtime resolution
- **Primary surface**: user input normalization for `ontobdc run`

## Purpose

This RFC proposes an optional hybrid interface layer that uses an LLM only as a text normalization boundary for highly conversational or chaotic user input.

The purpose is to support users who want a more open conversational interface without exposing the OntoBDC planning and execution core to:

- hallucinations
- opaque decision-making
- uncontrolled cloud token costs

## Context

The current OntoBDC runtime is increasingly structured around deterministic local components:

- runtime context materialization in RDF
- explicit FSM transitions
- DAG-based planning
- local capability validation
- local execution

That architecture is valuable because it remains:

- auditable
- testable
- bounded
- explainable

However, some users may still want to interact with the system in a much more conversational, open-ended, or linguistically chaotic way.

Supporting that style directly inside the deterministic parser can be difficult because:

- the input may be too noisy for lightweight local NLP
- the parser may receive text far outside its intended shape
- open-ended input can create large ambiguity before the system even reaches its structured stages

At the same time, delegating the whole run flow to an external generative model would be unacceptable because it would weaken determinism and auditability.

## Motivation

The project needs a way to support a more conversational front-end without surrendering architectural control to a commercial or opaque generative model.

The intended design principle is:

- LLM for interface flexibility
- local deterministic engine for actual reasoning and execution

This approach aims to deliver:

- better tolerance for chaotic user phrasing
- optional user-controlled experience upgrades
- protection against hallucination leaking into planning and execution
- bounded token consumption by limiting LLM scope

## Proposal

Introduce an optional, feature-gated LLM interface layer that sits before the standard intent-resolution machine.

This layer should act only as a normalization interface.

Its responsibility is limited to:

- cleaning raw user text
- reorganizing highly chaotic input
- outputting a sanitized structured sentence suitable for the local parser

The LLM must not:

- choose capabilities directly
- build the execution DAG
- resolve dependencies
- validate the final target
- execute anything

### Proposed Runtime Contract

The flow would become:

1. raw user input
2. optional LLM normalization interface
3. sanitized structured text
4. local deterministic OntoBDC state machine
5. planning, DAG resolution, and execution entirely under local control

### Proposed Cut Guarantee

The architecture must enforce a strict cut after normalization.

That means:

- the LLM returns only the normalized string
- the normalized string becomes the next input to the regular local pipeline
- the LLM has no participation in later runtime decisions

This cut is the core safety property of the proposal.

### Proposed Configurability

The feature should be optional and parameterized through active project features or configuration.

Possible control points include:

- whether the LLM layer is enabled
- which provider or backend is allowed
- maximum token budget
- maximum prompt size
- when the fallback is activated
- whether the layer is available only for selected languages or profiles

The feature must remain user-configurable and easy to disable.

### Proposed Output Shape

The LLM should not return arbitrary JSON planning objects or hidden chain-of-thought style content.

The first version should prefer a narrow output contract such as:

- one normalized sentence
- one structured reformulation of the user command

Example conceptual transformation:

- chaotic raw input -> hygienized intent sentence

The normalized text then enters the same local path already used by:

- `resolution_to_parsed`
- `resolution_to_validated`
- `resolution_to_planned`
- `resolution_to_filled`

## Constraints

This layer should:

- be optional
- be explicitly feature-gated
- have bounded cost
- have bounded scope
- be easy to inspect and disable
- preserve the determinism of the local machine

It should not:

- replace the local planner
- replace the FSM
- produce execution decisions
- introduce hidden state into the core runtime
- become mandatory for standard usage

## Expected Impact

If implemented, this change would likely affect:

- runtime input preprocessing boundaries
- feature/configuration handling
- parsing-related documentation
- tests for normalized versus raw input paths

Likely implementation areas:

- `wip/src/ontobdc/run/plugin/capability/resolution_to_parsed.py`
- a future configuration surface for optional runtime features
- possibly a dedicated adapter layer for LLM-backed normalization

Likely documentation impact:

- `docs/documentation/spec/SPEC006_run_cli_context_resolution.md`
- `docs/documentation/spec/SPEC008_run_intent_resolution_state_machine.md`
- a future ADR if this becomes an accepted architectural boundary

Likely test impact:

- verify strict cut after normalization
- verify fallback to the normal local pipeline
- verify that no capability, DAG, or execution decision is delegated to the LLM layer

## Open Questions

- What exact configuration surface should enable or disable this feature?
- Should the LLM layer run always when enabled, or only after local normalization fails?
- What is the minimum safe output contract for the normalized sentence?
- Should the normalized text be persisted alongside the original input for auditability?
- Which local or remote backends are acceptable for the first version?
- How should token budget limits be enforced?

## Follow-Up

If accepted, the next step should be to define:

- the exact feature flag model
- the minimal LLM adapter contract
- the strict output schema for the normalized text
- the audit trail for original versus normalized input
- the tests that prove the LLM layer cannot influence planning or execution beyond text normalization
