# Documentation for `test_resolution_to_canonical.py`

## Test File

- Source: `test/src/ontobdc/run/plugin/capability/test_resolution_to_canonical.py`
- Unit under test: `ResolutionToCanonicalCapability`
- Style: `unittest` with `patch`

## What This File Tests

This document describes normalization of the user intent into a canonical form by combining spell correction and lemmatization before saving the result in the context.

## Documented Scenario

### `test_execute_creates_canonical_intent`

**What is tested**

- The text `helo wrld` goes through mocked spell correction.
- The corrected text goes through mocked lemmatization.
- Valid tokens are combined into a canonical string separated by `;`.

**Expected result**

- The `canonical_intent` parameter is set to `hello;world`.
- The main flow completes without raising an exception.

**What is mocked**

- `SpellChecker`, to control the corrections.
- `ResolutionToCanonicalCapability._load_spacy_model`, to avoid loading a real model.
- `spacy`, `spacy.tokens`, and `spellchecker` in `sys.modules`.
- The `nlp` object and the tokens returned in internal calls.

**What is not mocked**

- `ResolutionToCanonicalCapability`, executed for real.
- `CliContextAdapter`, used for real.
- The logic that builds the final canonical string.

## Notes

- The test covers only the happy path.
- There is no file persistence check; coverage is focused on the final value saved in the context.
