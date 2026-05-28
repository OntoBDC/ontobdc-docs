# RFC 002 - Grammatical Normalization And Noise Tolerance Layer Before Intent Parsing

## Status

- **Status**: requested
- **Scope**: text preprocessing before `resolution_to_parsed`
- **Primary surface**: `ontobdc run` intent parsing flow

## Purpose

This RFC proposes adding a lightweight text normalization layer before the current spaCy parsing step used by `resolution_to_parsed`.

The goal is to improve grammatical robustness for low-friction terminal input, especially when the user omits accentuation or introduces small orthographic noise in structurally important words.

## Context

The current parsing flow relies directly on a lightweight spaCy model such as `pt_core_news_sm`.

That model is fast and useful, but it can show grammatical short-sightedness when the user types noisy terminal input.

A concrete failure case already observed is the loss of accentuation in short grammatical terms, such as:

- `é` becoming `e`
- `são` becoming `sao`

In those cases, the dependency tree may degrade enough to:

- identify the wrong root
- classify a structural token incorrectly
- generate invalid or misleading triples in `context.rdf`
- mislead downstream capability validation and filtering

## Motivation

Terminal-oriented usage has a low barrier of entry and should tolerate imperfect input.

Users should not need perfect orthography to obtain a valid dependency structure for common operational intents.

This is especially important for:

- short interactive prompts
- fast command-line usage
- Portuguese grammatical markers that depend on accentuation
- structural terms whose misclassification can corrupt the parse tree

The intent parser should therefore accept a meaningful level of orthographic chaos without collapsing the grammatical backbone of the sentence.

## Proposal

Introduce a preprocessing stage before the current spaCy model call in `resolution_to_parsed`.

This new stage should:

1. receive the raw user intent text
2. apply a lightweight local normalization pass
3. return a normalized string for the parser
4. optionally preserve both original and normalized forms for debugging or RDF traceability

### Proposed Responsibilities

The preprocessing layer should focus on:

- grammatical normalization
- tolerance to small orthographic errors
- restoration of high-impact accentuation in structural tokens

### Proposed Normalization Strategy

Use a lightweight local orthographic normalizer, such as an edit-distance-based approach inspired by SymSpell, but constrained to a narrow linguistic scope.

The normalizer should prioritize:

- closed-class grammatical words
- common auxiliary verbs
- interrogative forms
- short structural terms that strongly affect dependency parsing

Examples of desirable corrections:

- `e` -> `é` when the surrounding structure strongly indicates the verb
- `sao` -> `são`
- `quais sao` -> `quais são`

### Proposed Tolerance Rules

The layer should be conservative.

It should:

- prefer low-risk corrections
- target structural grammar before general vocabulary
- avoid rewriting domain-specific nouns aggressively
- avoid turning the pre-parser into a full spell-checker

### Possible Runtime Contract

If implemented, the parsing flow may evolve into:

1. raw user input
2. grammatical normalization and noise tolerance
3. spaCy parsing
4. semantic mapping and RDF materialization

## Constraints

The preprocessing layer should:

- remain lightweight and local
- avoid network calls or external remote dependencies
- avoid introducing a heavy language-model dependency before spaCy
- remain explainable and testable
- minimize false positive rewrites
- work well for terminal-sized inputs rather than large text corpora

## Expected Impact

If implemented, this change would likely affect:

- `src/ontobdc/run/plugin/capability/resolution_to_parsed.py`
- parsing-related runtime tests
- RDF expectations for `parsedIntent`
- state-machine reliability when parsing noisy user input

Likely test impact:

- add cases for accent omission in Portuguese
- verify stable root extraction after normalization
- verify that `parsedIntent` remains semantically valid under noisy terminal input

Likely documentation impact:

- `documentation/spec/SPEC008_run_intent_resolution_state_machine.md`
- `documentation/test/TEST005_run_context_state_machine_tests.md`

## Open Questions

- Should the normalized text replace the original text entirely, or should both be preserved?
- Should normalization be language-specific from day one, or only for Portuguese initially?
- Should the correction layer operate only on a curated structural lexicon?
- How much correction confidence is required before rewriting a token?
- Should the RDF runtime artifact record that normalization occurred?

## Follow-Up

If accepted, the next step should be to define:

- the exact boundary between normalization and parsing
- the first structural lexicon for Portuguese
- the acceptance rules for conservative token correction
- the test corpus for noisy terminal inputs
