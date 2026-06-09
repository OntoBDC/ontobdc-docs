# Documentation for `test_resolution_from_low_confidence.py`

## Test File

- Source: `test/src/ontobdc/run/plugin/capability/test_resolution_from_low_confidence.py`
- Unit under test: `ResolutionFromLowConfidenceCapability`
- Style: `unittest` with `patch`

## What This File Tests

This document describes the step executed when the intent still has low confidence and the system attempts to find compatible capabilities from the canonical intent and the parse returned by the resolver.

## Documented Scenario

### `test_execute_finds_matching_capabilities`

**What is tested**

- The capability runs its main flow with `context_language`, `user_intent`, and `canonical_intent` defined.
- The NLP resolver returns an `IntentScoreResponse` with score `0.8` and a valid nominal root.
- The capability loader returns a dummy candidate capability.
- The execution attempts to persist the canonical intent result in the configuration directory.

**Expected result**

- `result["cli_context"].get_parameter_value("intent_score")` returns `0.8`.
- The file `IntentScoreResponse.CANONICALIZED_INTENT_FILE_NAME` exists in the temporary directory.
- The flow completes without raising an exception.

**What is mocked**

- `SpacyIntentModelResolver`, to control `parse_intent()`.
- `CapabilityLoader`, to control the available capabilities.
- `get_config_dir`, to isolate file output in a temporary directory.
- `spacy` and `spacy.tokens`, injected into `sys.modules` before import.

**What is not mocked**

- `ResolutionFromLowConfidenceCapability`, executed for real.
- `CliContextAdapter`, used for real.
- `IntentScoreResponse`, instantiated for real.
- File output inside `tempfile.TemporaryDirectory()`.
- `DummyQueryCapability`, used as a simple concrete implementation.

## Notes

- The test covers the happy path.
- The assertion verifies the score and file existence, but does not validate the saved file contents.
