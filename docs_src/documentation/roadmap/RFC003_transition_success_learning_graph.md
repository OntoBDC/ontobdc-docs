# RFC 003 - Transition Success Learning Graph As An Auditable Semantic Cache

## Status

- **Status**: requested
- **Scope**: long-term runtime learning artifact for `ontobdc run`
- **Primary surface**: intent resolution, validation, and historical memory reuse

## Purpose

This RFC proposes a persistent long-term learning artifact that records successful intent-resolution outcomes without depending on opaque statistical fine-tuning.

The goal is to let the system recognize local jargon, repeated linguistic shortcuts, and stable team-specific expressions while preserving:

- determinism
- auditability
- explicit persistence rules
- graph-native inspection

## Context

The current run intent-resolution flow already materializes runtime state in `context.rdf` and advances through a deterministic FSM until the final `FILLED` state.

That architecture provides a strong foundation for controlled learning because:

- transitions are explicit
- success has a well-defined final state
- resolved capability IDs are materialized
- runtime artifacts are already RDF-oriented

However, the system still lacks a persistent historical memory capable of capturing successful linguistic patterns over time.

As a result:

- local jargon has to be rediscovered repeatedly
- recurring phrasing does not accumulate operational value
- the system cannot safely reuse proven transition outcomes
- clarification costs remain unnecessarily high for repeated successful intents

## Motivation

The project needs a continuous learning mechanism that is:

- local
- interpretable
- deterministic
- inspectable on disk

The goal is not to build a black-box language adaptation layer.

Instead, the goal is to build an auditable semantic cache that remembers which raw linguistic patterns consistently led to which resolved capability.

This is especially useful in environments where:

- teams reuse internal jargon
- commands are short and informal
- users repeat similar intent patterns over time
- maintainers need to inspect why a shortcut was learned

## Proposal

Introduce a persistent artifact named `memory.rdf` as a long-term historical memory graph for successful intent-resolution outcomes.

This artifact should store pairings of:

- raw linguistic pattern
- resolved capability ID

The artifact should only be updated when the run intent-resolution FSM reaches `FILLED` successfully.

### Proposed Artifact

Suggested artifact:

- `.__ontobdc__/memory.rdf`

Suggested role:

- long-term semantic memory
- auditable success history
- weighted historical graph for reused linguistic paths

### Proposed Persistence Rule

The system should persist a new historical pairing only when:

1. a raw user linguistic pattern is present
2. a `capability_id` has been resolved
3. the FSM reaches `FILLED`
4. the transition is considered successful and stable enough to record

This rule intentionally avoids learning from:

- partial flows
- failed runs
- low-confidence exploratory states
- contexts that never reached final resolution

### Proposed Learning Unit

The minimum learning unit should be:

- `[Raw Linguistic Pattern] -> [Resolved Capability_ID]`

Possible examples of raw pattern sources:

- `userIntent`
- normalized intent text if a future normalization layer is adopted
- selected parsed-root summary in later evolutions

The first version should stay minimal and explicit.

### Proposed Weighted Graph Model

The historical memory should support weighted edges so the system can compute usage frequency and confidence from repeated successful resolutions.

Conceptually:

- nodes represent linguistic patterns and capability IDs
- edges represent successful pairings
- weights increase as the same successful pairing recurs

This weighted graph would allow the system to:

- rank historically successful mappings
- identify stable local jargon
- prefer proven capability paths
- remain explainable because the learned relationship is explicit

### Proposed Runtime Use

If implemented, `resolution_to_validated` could consult the historical memory graph before or during final capability validation.

That consultation could allow the runtime to:

- boost candidate capability confidence when the pattern has strong historical evidence
- skip some clarification steps when the historical path is sufficiently strong
- keep the decision statistically safer without delegating control to an opaque model

The intended effect is not unrestricted shortcutting.

It is a constrained reuse of historically successful paths.

## Constraints

This learning mechanism should:

- remain deterministic
- remain auditable
- persist only on successful final outcomes
- avoid hidden model adaptation
- avoid remote dependency or opaque external scoring
- preserve graph-level inspectability
- define explicit thresholds before historical evidence can affect runtime decisions

It should not:

- behave like silent fine-tuning
- rewrite user intent invisibly without trace
- learn from failed or incomplete runs
- override explicit capability targeting by the user

## Expected Impact

If implemented, this change would likely affect:

- `src/ontobdc/run/adapter/machine.py`
- `src/ontobdc/run/plugin/capability/resolution_to_validated.py`
- final-state transition handling around `FILLED`
- RDF persistence rules for runtime learning artifacts

Likely new or updated artifacts:

- `.__ontobdc__/memory.rdf`
- ontology definitions for long-term semantic memory
- tests for successful persistence only on `FILLED`

Likely documentation impact:

- `documentation/spec/SPEC007_ontobdc_context.md`
- `documentation/spec/SPEC008_run_intent_resolution_state_machine.md`
- a future ADR if the memory graph becomes an accepted architectural decision

## Open Questions

- What is the canonical definition of a raw linguistic pattern in the first version?
- Should the memory graph store only raw text, or also normalized text once a pre-parser exists?
- What threshold should be required before historical weight can influence validation?
- Should the graph decay old weights, or remain cumulative?
- Should the memory be project-local only, or also support shared team memory later?
- How should maintainers inspect, prune, or reset learned history?

## Follow-Up

If accepted, the next step should be to define:

- the RDF model for `memory.rdf`
- the exact success criteria for persistence at `FILLED`
- the weighting algorithm for repeated successful mappings
- the safety threshold for allowing historical evidence to influence `resolution_to_validated`
- the test strategy for deterministic and auditable learning behavior
