# RFC 005 - OLiA Mapper Extraction And Graph-Based Intent Inference Completion

## Status

- **Status**: requested
- **Scope**: completion of the OLiA architecture in the `ontobdc run` intent-resolution flow
- **Primary surface**: `resolution_to_parsed`, `resolution_to_validated`, RDF parsed-intent semantics, and graph-based intent inference

## Purpose

This RFC proposes the completion of the current OLiA integration already present in the runtime.

The goal is to move from a partially embedded OLiA usage model to a clearer architectural boundary with:

- a dedicated linguistic mapper
- a more explicit semantic contract for parsed intent items
- graph-based inference for intent classification during `PARSED -> VALIDATED`

This RFC builds directly on the implemented baseline documented in:

- [SPEC009_olia_semantic_intent_typing.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC009_olia_semantic_intent_typing.md)

## Context

The current runtime already uses OLiA in meaningful ways.

Today, the system already:

- maps selected spaCy `POS` and `PronType=Int` signals to OLiA URIs
- persists those URIs as `rdf:type` inside nested `parsedIntent` nodes in `context.rdf`
- restores those URIs during RDF round-trip
- uses OLiA-derived signals in `resolution_to_validated` to filter query and action capabilities

That baseline is valuable, but it remains incomplete because:

- the mapping logic is still embedded in `ResolutionToParsedCapability`
- the semantic contract is only partial
- capability filtering still depends on direct in-memory heuristics rather than graph-native inference
- the current design does not yet provide a reusable OLiA abstraction for future languages

## Motivation

The project should avoid hardcoded interrogative word lists and language-specific textual shortcuts as more languages are added.

The current OLiA baseline already points in the right direction, but the architecture is not yet complete enough to serve as the universal linguistic layer envisioned by the design.

The missing pieces matter because they affect:

- extensibility across languages
- reuse of the mapping logic outside a single capability
- auditability of linguistic inference rules
- the ability to evolve from local heuristics to graph-native semantic queries

## Proposal

Complete the OLiA integration in three coordinated steps:

1. extract a dedicated `OliaLinguisticMapper`
2. formalize an OLiA-first parsed-intent contract
3. replace direct validation heuristics with graph-based intent inference

### Proposed Step 1 - Extract `OliaLinguisticMapper`

The current inline `MAPPER_OLIA` and `_resolve_olia_token()` logic should be extracted into a dedicated component.

Suggested responsibility of `OliaLinguisticMapper`:

- receive a spaCy token
- inspect `POS` and morphological features
- resolve the best matching OLiA URI
- expose a stable, reusable contract for future parsers and languages

The first version may still remain spaCy-oriented, but the mapping logic should no longer be buried inside `ResolutionToParsedCapability`.

This extraction should make it easier to:

- expand mapping coverage
- test linguistic mapping independently
- reuse the mapper from multiple runtime surfaces

### Proposed Step 2 - Formalize The Semantic Contract

The parsed intent model should evolve from a mixed textual structure with optional semantic typing into a clearer semantic contract.

This does not require deleting all raw textual fields immediately.

However, the decision-making contract should become OLiA-first.

That means:

- OLiA typing becomes the primary semantic signal for intent reasoning
- raw text remains auxiliary for debugging, traceability, and human inspection
- the RDF representation documents semantic class membership explicitly and consistently

The project may keep fields such as:

- `itemText`
- `itemPos`
- `itemLemma`
- `itemHead`

but runtime reasoning should progressively stop depending on those raw values when a semantic alternative is available.

### Proposed Step 3 - Graph-Based Intent Inference

The current `PARSED -> VALIDATED` reasoning should move away from direct in-memory heuristics over token dictionaries.

The target is graph-based inference over the parsed-intent structure already materialized in RDF.

The first completion version should support reasoning such as:

- detect whether a parsed item is typed as `olia:InterrogativePronoun`
- detect whether that item is linked to the root structure in a query-relevant way
- infer whether the intent is query-oriented or action-oriented using semantic graph patterns

The query mechanism may be implemented through:

- SPARQL over the loaded graph
- or an equivalent graph-query abstraction with the same semantic effect

The important contract is not the syntax itself.

The important contract is that intent classification becomes graph-native and ontology-oriented instead of ad hoc dictionary inspection.

## Proposed Runtime Boundary

The intended runtime shape becomes:

1. raw user input
2. spaCy parsing
3. `OliaLinguisticMapper` assigns semantic classes
4. parsed intent is materialized in RDF with explicit OLiA typing
5. the `PARSED -> VALIDATED` layer infers query versus action semantics through graph-native reasoning
6. capability filtering consumes that inference result

This RFC does not propose moving that reasoning into `ContextIntentEvaluatorAdapter` as it currently exists.

That adapter is presently a lifecycle-state detector.

The target boundary is the logic that decides candidate capability class during the `PARSED -> VALIDATED` transition, whether that remains in `resolution_to_validated` or is delegated to a dedicated query service.

## Constraints

The completed OLiA architecture should:

- remain deterministic
- remain local and auditable
- avoid language-specific hardcoded word lists as the primary decision mechanism
- keep graph semantics inspectable in `context.rdf`
- remain compatible with the current nested RDF materialization model
- be testable independently at mapper level and transition-inference level

It should not:

- introduce opaque statistical inference as the primary linguistic decision layer
- bypass the deterministic capability-selection flow
- depend on remote linguistic services
- turn raw text into the main source of truth when OLiA typing is available

## Expected Impact

If implemented, this RFC would likely affect:

- `src/ontobdc/run/plugin/capability/resolution_to_parsed.py`
- `src/ontobdc/run/plugin/capability/resolution_to_validated.py`
- `src/ontobdc/run/adapter/machine.py`
- a new dedicated OLiA mapping module or adapter

Likely new or updated tests:

- mapper-level tests for `POS` and morphology to OLiA URI resolution
- RDF round-trip tests for expanded OLiA coverage
- validation tests proving graph-based query versus action inference
- language-extensibility tests that avoid hardcoded interrogative word lists

Likely documentation impact:

- [SPEC009_olia_semantic_intent_typing.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/spec/SPEC009_olia_semantic_intent_typing.md)
- `docs/documentation/spec/SPEC006_run_cli_context_resolution.md`
- future test documentation for parser and validator coverage

## Correlation With SPEC009

`SPEC009` documents what already exists.

This RFC proposes what should be added or refactored next.

The main correlation is:

- `SPEC009`: inline OLiA mapping in `ResolutionToParsedCapability`
- `RFC005`: extract that logic into `OliaLinguisticMapper`

- `SPEC009`: parsed items carry both raw text and OLiA `uri`
- `RFC005`: keep both if needed, but make OLiA the primary reasoning contract

- `SPEC009`: capability filtering uses direct URI and head-text heuristics
- `RFC005`: move to graph-native semantic inference

- `SPEC009`: `ContextIntentEvaluatorAdapter` only detects materialized runtime state
- `RFC005`: keep state evaluation separate and evolve the `PARSED -> VALIDATED` reasoning boundary instead

The intended migration rule is:

- treat `SPEC009` as the baseline that must remain true until code changes land
- update `SPEC009` after each accepted part of this RFC becomes current behavior

## Open Questions

- Should graph-native reasoning be implemented directly with SPARQL, or wrapped behind a query adapter?
- What is the minimum OLiA class coverage required before the mapper is considered reusable across languages?
- Should dependency heads remain textual, or should they also evolve toward semantic node references?
- Should the inferred intent class be materialized explicitly in `context.rdf`, or remain derived at runtime?
- Which additional OLiA classes are most valuable after interrogative pronouns and verbs?

## Follow-Up

If accepted, the next step should be to define:

- the interface of `OliaLinguisticMapper`
- the first expanded mapping table and test corpus
- the graph query contract for query-versus-action inference
- the migration plan from direct heuristics to graph-native reasoning
- the exact RDF invariants that must hold after the refactor
