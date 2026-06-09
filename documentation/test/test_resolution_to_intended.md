# Documentation for `test_resolution_to_intended.py`

## Test File

- Source: `test/src/ontobdc/run/plugin/capability/test_resolution_to_intended.py`
- Unit under test: `ResolutionToIntendedCapability`
- Style: `unittest` with injected prompt

## What This File Tests

This document describes the initial stage in which the system asks the user to describe their intent, stores that text in the context, and fails when the input is invalid or when the required prompt has not been configured.

## Documented Scenarios

### `test_execute_prompts_user_and_sets_intent`

**What is tested**

- The raw text prompt is injected into the capability.
- The prompt returns a valid user phrase.
- The capability stores that value in `user_intent`.

**Expected result**

- The `user_intent` parameter is set to `I need help`.
- The flow completes without error.

**What is mocked**

- The interactive prompt, through `set_prompt_raw_text`.

**What is not mocked**

- `ResolutionToIntendedCapability`.
- `CliContextAdapter`.
- The real logic that stores the intent in the context.

### `test_execute_raises_error_on_empty_intent`

**What is tested**

- The prompt returns an empty string.
- The capability must reject the input.

**Expected result**

- Execution raises `ValueError`.
- No valid intent is accepted by the flow.

**What is mocked**

- The interactive prompt, configured to return an empty string.

**What is not mocked**

- `ResolutionToIntendedCapability`.
- `CliContextAdapter`.
- The real rule that treats an empty intent as an error.

### `test_execute_raises_error_if_prompt_not_set`

**What is tested**

- The capability is executed without injecting the prompt.

**Expected result**

- Execution raises `RuntimeError`.
- The test guarantees that the prompt dependency is required.

**What is mocked**

- Nothing in this scenario.

**What is not mocked**

- `ResolutionToIntendedCapability`, including its precondition validation.
- `CliContextAdapter`.

## Notes

- This is the file with the lowest level of mocking among the documented tests.
- Coverage is focused on interaction and input validation.
