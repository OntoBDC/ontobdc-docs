# Documentation for `test_resolution_to_validated.py`

## Test File

- Source: `test/src/ontobdc/run/plugin/capability/test_resolution_to_validated.py`
- Unit under test: `ResolutionToValidatedCapability`
- Style: `unittest` with `patch` and injected prompt

## What This File Tests

This document describes the validation stage in which the user chooses one capability from the previously found matches, converting that choice into `selected_capability_id`.

## Documented Scenario

### `test_execute_prompts_user_to_select_capability`

**What is tested**

- The test creates a real canonical intent file containing `matching_capabilities`.
- `CapabilityLoader` returns a resolvable dummy capability.
- The choice prompt is mocked to return `Test`.
- The capability transforms the user choice into a selected identifier in the context.

**Expected result**

- The `selected_capability_id` parameter is set to `org.example.capability.test`.
- The validation flow completes without error.

**What is mocked**

- `CapabilityLoader`.
- `get_config_dir`, to isolate the file in a temporary directory.
- The interactive prompt, injected through `set_prompt_choice`.

**What is not mocked**

- `ResolutionToValidatedCapability`.
- `CliContextAdapter`.
- `IntentScoreResponse`, used for real to serialize the input file.
- Real reading of the JSON file saved in the temporary directory.
- `DummyQueryCapability`, used as a simple concrete implementation.

## Notes

- The test covers only the case where a valid option exists and the user chooses the expected label.
- There is no coverage for cancellation, invalid selection, or multiple ambiguous options.
