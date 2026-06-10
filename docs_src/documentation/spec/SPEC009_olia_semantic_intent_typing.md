# SPEC 009 - OLiA Semantic Intent Typing In The Current Run Runtime

## Status

- **Status**: Working specification of the current OLiA-based semantic typing behavior
- **Scope**: `src/ontobdc/run/plugin/capability/resolution_to_parsed.py`, `src/ontobdc/run/plugin/capability/resolution_to_validated.py`, and `src/ontobdc/run/adapter/machine.py`
- **Audience**: maintainers and contributors working on intent parsing, RDF materialization, and capability filtering

## 1. Purpose

This specification describes the OLiA-related behavior that is already implemented in the current `ontobdc run` intent-resolution flow.

The goal of this document is to define the current baseline for:

- semantic typing of parsed linguistic items using OLiA URIs
- persistence of those types in `context.rdf`
- round-trip reconstruction of typed parsed intent structures
- capability filtering decisions that already consume OLiA-derived signals

This specification documents the current working runtime.

It does not describe the intended future completion of the OLiA architecture.

That forward-looking work is proposed in:

- [RFC005_olia_inference_and_mapper_completion.md](file:///Users/eliasmpjunior/infobim/deploy/ontobdc-stack/docs/documentation/roadmap/RFC005_olia_inference_and_mapper_completion.md)

## 2. Source Of Truth

This specification is derived from the current implementation under:

- `src/ontobdc/run/plugin/capability/resolution_to_parsed.py`
- `src/ontobdc/run/plugin/capability/resolution_to_validated.py`
- `src/ontobdc/run/adapter/machine.py`

The active automated tests covering this behavior are:

- `test/src/ontobdc/run/adapter/test_machine.py`

## 3. Runtime Role

In the current runtime, OLiA acts as a semantic typing layer attached to the parsed intent structure produced by spaCy.

Its current role is limited to:

- mapping selected spaCy token signals to OLiA URIs
- persisting those URIs into `context.rdf`
- restoring them when `context.rdf` is loaded again
- using those URIs as signals during capability filtering in the `PARSED -> VALIDATED` transition path

The current implementation does not delegate planning, DAG construction, or execution to OLiA.

## 4. Current Typing Model

### 4.1 Typing Boundary

The current OLiA mapping boundary lives inside `ResolutionToParsedCapability`.

The parser:

1. loads the configured spaCy model
2. parses the user intent text
3. builds `IntentScoreResponse`
4. assigns an OLiA URI to each relevant parsed item through `_resolve_olia_token()`

### 4.2 Current Mapping Mechanism

The current implementation uses an inline mapping table named `MAPPER_OLIA`.

It maps selected `POS` and morphological combinations to OLiA classes.

The implemented mappings currently include:

- `("PRON", "PronType=Int") -> olia:InterrogativePronoun`
- `("DET", "PronType=Int") -> olia:InterrogativePronoun`
- `("ADV", "PronType=Int") -> olia:InterrogativeAdverb`
- `("NOUN", None) -> olia:Noun`
- `("VERB", None) -> olia:Verb`
- `("PRON", None) -> olia:Pronoun`
- `("ADV", None) -> olia:Adverb`
- `("PUNCT", None) -> olia:Punctuation`

If no explicit mapping exists, the parser falls back to:

- `olia:LinguisticSign`

### 4.3 Current Interrogative Detection Rule

The current interrogative rule is derived from spaCy morphology.

A token is treated as interrogative when:

- `PronType=Int` is present in `token.morph`

When that flag is present, the parser attempts the specific OLiA match before falling back to the base class for the token `POS`.

## 5. Parsed Intent Contract

The current parsed intent artifact is `IntentScoreResponse`.

Its OLiA-aware structures currently include:

- `pos_tags`
- `dependencies`
- `roots`

Each item may carry both textual and semantic information.

### 5.1 `pos_tags`

Each `pos_tag` entry may contain:

- `text`
- `pos`
- `uri`

### 5.2 `dependencies`

Each dependency entry may contain:

- `text`
- `dep`
- `head`
- `uri`

### 5.3 `roots`

Each root entry may contain:

- `text`
- `pos`
- `lemma`
- `uri`

### 5.4 Current Contract Semantics

The current runtime is not OLiA-only.

It preserves raw linguistic fields such as:

- `text`
- `pos`
- `dep`
- `head`
- `lemma`

and augments them with:

- `uri`

This means semantic typing currently complements, rather than replaces, the raw textual representation.

## 6. RDF Materialization In `context.rdf`

### 6.1 Serialization Model

When `parsed_intent` is serialized into `context.rdf`, the OLiA URI is materialized as `rdf:type` on the nested nodes that represent:

- `hasPosTag`
- `hasDependency`
- `hasRoot`

The current serializer does not create a separate OLiA property.

Instead, it stores the semantic type directly as RDF class membership of the nested item node.

### 6.2 Round-Trip Model

When `context.rdf` is loaded again:

- nested parsed-intent nodes are traversed
- `rdf:type` is read back
- the detected type is restored into the in-memory item as `uri`

This preserves the OLiA semantic signal across serialization and deserialization.

## 7. Current `PARSED -> VALIDATED` Use Of OLiA

### 7.1 Transition Boundary

The current OLiA-based intent inference does not live in `ContextIntentEvaluatorAdapter`.

That adapter currently evaluates which lifecycle state is already materialized in `context.rdf`.

The actual OLiA-aware filtering logic currently lives in:

- `ResolutionToValidatedCapability`

### 7.2 Implemented Query-Oriented Heuristic

The current validation layer checks whether a dependency item typed as:

- `olia:InterrogativePronoun`

is linked to a current root through the dependency `head` text.

If that condition is satisfied, the candidate capabilities are narrowed to:

- subclasses of `QueryCapability`

### 7.3 Implemented Action-Oriented Heuristic

The validation layer also checks whether a dependency item typed as:

- `olia:Pronoun`

is linked to a root typed as:

- `olia:Verb`

If that condition is satisfied, the candidate capabilities are narrowed to:

- subclasses of `ActionCapability`

### 7.4 Current Decision Style

The current implementation already avoids hardcoded interrogative word lists in the decision step.

However, it still uses direct in-memory comparisons over:

- item `uri`
- dependency `head`
- root `text`

It does not perform SPARQL queries or ontology-class inference over the graph.

## 8. Test Coverage Summary

The current automated tests validate at least the following OLiA-related behavior:

- `parsed_intent` nested nodes preserve `rdf:type` resources
- `olia:InterrogativePronoun` survives RDF round-trip
- the nested `context.rdf` shape can be read back into `IntentScoreResponse`

The most direct OLiA persistence coverage currently lives in:

- `test_load_preserves_rdf_type_resources_inside_nested_nodes`
- `test_cli_context_reads_current_nested_context_shape`

both located in:

- `test/src/ontobdc/run/adapter/test_machine.py`

## 9. Current Limitations

The current implementation has important limitations that remain outside this working specification.

- The mapping layer is embedded directly in `ResolutionToParsedCapability`; there is no dedicated `OliaLinguisticMapper`.
- OLiA typing is partial and currently covers only a narrow subset of token classes and interrogative patterns.
- Raw fields such as `itemPos` and `itemText` remain first-class runtime data; they were not replaced by a fully semantic contract.
- Validation uses direct URI comparisons and dependency-head string matching; it does not use SPARQL or graph-class reasoning.
- `ContextIntentEvaluatorAdapter` remains a state detector, not an ontological intent classifier.

## 10. Correlation With RFC005

`SPEC009` defines the implemented baseline.

`RFC005` defines the architectural completion still proposed for that baseline.

The relationship is:

- `SPEC009` documents that OLiA typing already exists in the parser, RDF serialization, and capability filtering
- `RFC005` proposes extracting that logic into a dedicated mapper and formalizing graph-level inference
- `SPEC009` documents that raw linguistic fields are still preserved
- `RFC005` proposes an OLiA-first contract for decision-making while keeping raw text only as auxiliary trace data
- `SPEC009` documents direct URI-based heuristics in `resolution_to_validated`
- `RFC005` proposes replacing or encapsulating those heuristics behind graph-query-based inference

The intended maintenance rule is:

- update `SPEC009` when current runtime behavior changes
- update `RFC005` only while the completion work remains proposed and not fully merged
