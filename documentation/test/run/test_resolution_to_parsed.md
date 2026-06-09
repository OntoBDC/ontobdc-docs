# Documentation for `test_resolution_to_parsed.py`

## Test File

- Source: `test/src/ontobdc/run/plugin/capability/test_resolution_to_parsed.py`
- Unit under test: `ResolutionToParsedCapability`
- Style: `unittest` with `patch`

## What This File Tests

This document describes the step that interprets the user intent, produces an `IntentScoreResponse`, saves the parse to disk, and adjusts the confidence score in the context.

## Documented Scenarios

### `test_execute_parses_intent_and_saves_to_file`

**What is tested**

- The capability processes `user_intent` with a mocked NLP resolver.
- The parse returns a root with `pos = "NOUN"`, which is considered valid.
- The parsed result is saved in the configuration directory.

**Expected result**

- The file `IntentScoreResponse.PARSED_INTENT_FILE_NAME` exists in the temporary directory.
- The `intent_score` parameter is set to `0.8`.
- The flow ends without error.

**What is mocked**

- `SpacyIntentModelResolver`.
- `get_config_dir`.
- `spacy` and `spacy.tokens` in `sys.modules`.

**What is not mocked**

- `ResolutionToParsedCapability`.
- `CliContextAdapter`.
- `IntentScoreResponse`.
- Real file output in the temporary directory.

### `test_execute_no_noun_roots_sets_score_zero`

**What is tested**

- The parse returns a root with `pos = "VERB"` instead of `NOUN`.
- The capability must lower the score because no suitable nominal root is found.

**Expected result**

- The `intent_score` parameter is set to `0.0`.
- The flow demonstrates the confidence downgrade rule.

**What is mocked**

- `SpacyIntentModelResolver`.
- `get_config_dir`.
- `spacy` and `spacy.tokens` in `sys.modules`.

**What is not mocked**

- `ResolutionToParsedCapability`.
- `CliContextAdapter`.
- `IntentScoreResponse`.
- The real logic that sets the score to zero when roots do not match the expected criteria.

## Notes

- This file covers both persistence and parse qualification rules.
- The second test does not explicitly verify file persistence.
